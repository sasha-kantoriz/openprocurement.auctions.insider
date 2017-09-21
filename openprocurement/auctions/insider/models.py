# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
from schematics.types import StringType
from schematics.types.compound import ModelType
from schematics.exceptions import ValidationError
from schematics.transforms import whitelist
from schematics.types.serializable import serializable
from zope.interface import implementer
from openprocurement.api.models import (
    Model, ListType
)

from openprocurement.api.utils import calculate_business_date
from openprocurement.api.models import get_now, Value, Period
from openprocurement.auctions.core.models import IAuction
from openprocurement.auctions.flash.models import calc_auction_end_time
from openprocurement.auctions.dgf.models import (
    DGFFinancialAssets as BaseAuction,
    get_auction, Bid as BaseBid,
    Organization,
    AuctionAuctionPeriod as BaseAuctionPeriod,
    DGF_PLATFORM_LEGAL_DETAILS,
    rounding_shouldStartAfter,
)

from openprocurement.auctions.insider.utils import generate_auction_url


DUTCH_PERIOD = timedelta(hours=5)

class AuctionAuctionPeriod(BaseAuctionPeriod):
    """The auction period."""

    @serializable(serialize_when_none=False)
    def shouldStartAfter(self):
        if self.endDate:
            return
        auction = self.__parent__
        if self.startDate and get_now() > calc_auction_end_time(auction.numberOfBids, self.startDate):
            start_after = calc_auction_end_time(auction.numberOfBids, self.startDate)
        elif auction.enquiryPeriod and auction.enquiryPeriod.endDate:
            start_after = auction.enquiryPeriod.endDate
        else:
            return
        return rounding_shouldStartAfter(start_after, auction).isoformat()

    def validate_startDate(self, data, startDate):
        auction = get_auction(data['__parent__'])
        if not auction.revisions and not startDate:
            raise ValidationError(u'This field is required.')


class Bid(BaseBid):
    tenderers = ListType(ModelType(Organization), required=True, min_size=1, max_size=1)

    class Options:
        roles = {
            'create': whitelist('tenderers', 'parameters', 'lotValues', 'status', 'qualified', 'eligible'),
        }

    def validate_value(self, data, value):
        if isinstance(data['__parent__'], Model):
            auction = data['__parent__']
            if not value:
                return
            if auction.get('value').currency != value.currency:
                raise ValidationError(u"currency of bid should be identical to currency of value of auction")
            if auction.get('value').valueAddedTaxIncluded != value.valueAddedTaxIncluded:
                raise ValidationError(u"valueAddedTaxIncluded of bid should be identical to valueAddedTaxIncluded of value of auction")

    @serializable(serialized_name="participationUrl", serialize_when_none=False)
    def participation_url(self):
        if not self.participationUrl and self.status != "draft":
            request = get_auction(self).__parent__.request
            url = generate_auction_url(request, bid_id=self.id)
            return url


@implementer(IAuction)
class Auction(BaseAuction):
    """Data regarding auction process - publicly inviting prospective contractors to submit bids for evaluation and selecting a winner or winners."""
    procurementMethodType = StringType(default="dgfInsider")
    bids = ListType(ModelType(Bid), default=list())  # A list of all the companies who entered submissions for the auction.
    auctionPeriod = ModelType(AuctionAuctionPeriod, required=True, default={})
    minimalStep = ModelType(Value)

    def initialize(self):
        if not self.enquiryPeriod:
            self.enquiryPeriod = type(self).enquiryPeriod.model_class()
        if not self.tenderPeriod:
            self.tenderPeriod = type(self).tenderPeriod.model_class()
        now = get_now()
        self.tenderPeriod.startDate = self.enquiryPeriod.startDate = now
        pause_between_periods = self.auctionPeriod.startDate - (self.auctionPeriod.startDate.replace(hour=20, minute=0, second=0, microsecond=0) - timedelta(days=1))
        self.enquiryPeriod.endDate = calculate_business_date(self.auctionPeriod.startDate, -pause_between_periods, self)
        pause_between_periods = self.auctionPeriod.startDate.replace(hour=16, minute=0, second=0, microsecond=0) - self.enquiryPeriod.endDate
        self.tenderPeriod.endDate = calculate_business_date(self.enquiryPeriod.endDate, pause_between_periods, self)
        self.auctionPeriod.startDate = None
        self.auctionPeriod.endDate = None
        self.date = now
        self.documents.append(type(self).documents.model_class(DGF_PLATFORM_LEGAL_DETAILS))

    @serializable(serialized_name="minimalStep", type=ModelType(Value))
    def auction_minimalStep(self):
        return Value(dict(amount=0))

    # @serializable(serialized_name="tenderPeriod", type=ModelType(Period))
    # def tender_Period(self):
    #     if self.tenderPeriod and self.auctionPeriod.startDate:
    #         pause_between_periods = (self.enquiryPeriod.endDate.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1) + DUTCH_PERIOD) - self.enquiryPeriod.endDate
    #         self.tenderPeriod.endDate = calculate_business_date(self.enquiryPeriod.endDate, pause_between_periods, self)
    #     return self.tenderPeriod


DGFInsider = Auction
