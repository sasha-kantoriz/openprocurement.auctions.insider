# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
from schematics.types import StringType
from schematics.types.compound import ModelType
from schematics.exceptions import ValidationError
from schematics.transforms import  whitelist
from schematics.types.serializable import serializable
from zope.interface import implementer
from openprocurement.api.models import (
    Model, ListType
)
from openprocurement.api.models import TZ, get_now, SANDBOX_MODE
from openprocurement.api.utils import calculate_business_date
from openprocurement.auctions.core.models import IAuction
from openprocurement.auctions.flash.models import calc_auction_end_time
from openprocurement.auctions.dgf.models import (
    DGFFinancialAssets as BaseAuction,
    get_auction, Bid as BaseBid,
    Organization,
    AuctionAuctionPeriod as BaseAuctionPeriod,

)

from openprocurement.auctions.insider.utils import generate_participation_url, DUTCH_PERIOD



AUCTION_START = timedelta(0, 36000)
DGF_PLATFORM_LEGAL_DETAILS = {
    'url': 'http://torgi.fg.gov.ua/prozorrosale',
    'title': u'Місце та форма прийому заяв на участь в аукціоні та банківські реквізити для зарахування гарантійних внесків',
    'documentType': 'x_dgfPlatformLegalDetails',
}

def rounding_shouldStartAfter(start_after, auction, use_from=datetime(2016, 6, 1, tzinfo=TZ)):
    if (auction.enquiryPeriod and auction.enquiryPeriod.startDate or get_now()) > use_from and not (SANDBOX_MODE and auction.submissionMethodDetails and u'quick' in auction.submissionMethodDetails):
        start_after = datetime.combine(start_after.date(), time(9, tzinfo=start_after.tzinfo))
    return start_after


class AuctionAuctionPeriod(BaseAuctionPeriod):
    """The auction period."""

    @serializable(serialize_when_none=False)
    def shouldStartAfter(self):
        if self.endDate:
            return
        auction = self.__parent__
        if auction.lots or auction.status not in ['active.tendering', 'active.auction']:
            return
        if self.startDate and get_now() > calc_auction_end_time(auction.numberOfBids, self.startDate):
            start_after = calc_auction_end_time(auction.numberOfBids, self.startDate)
        elif auction.tenderPeriod and auction.tenderPeriod.endDate:
            start_after = calculate_business_date(auction.tenderPeriod.endDate, -DUTCH_PERIOD, auction)
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
            if auction.lots:
                if value:
                    raise ValidationError(u"value should be posted for each lot of bid")
            else:
                if not value:
                    return
                if auction.value.amount > value.amount:
                    raise ValidationError(u"value of bid should be greater than value of auction")
                if auction.get('value').currency != value.currency:
                    raise ValidationError(u"currency of bid should be identical to currency of value of auction")
                if auction.get('value').valueAddedTaxIncluded != value.valueAddedTaxIncluded:
                    raise ValidationError(u"valueAddedTaxIncluded of bid should be identical to valueAddedTaxIncluded of value of auction")

    @serializable(serialized_name="participationUrl", serialize_when_none=False)
    def participation_url(self):
        if not self.participationUrl and self.status != "draft":
            request = get_auction(self).__parent__.request
            url = generate_participation_url(request, self.id)
            return url


@implementer(IAuction)
class Auction(BaseAuction):
    """Data regarding auction process - publicly inviting prospective contractors to submit bids for evaluation and selecting a winner or winners."""
    procurementMethodType = StringType(default="dgfInsider")
    bids = ListType(ModelType(Bid), default=list())  # A list of all the companies who entered submissions for the auction.
    auctionPeriod = ModelType(AuctionAuctionPeriod, required=True, default={})

    def initialize(self):
        if not self.enquiryPeriod:
            self.enquiryPeriod = type(self).enquiryPeriod.model_class()
        if not self.tenderPeriod:
            self.tenderPeriod = type(self).tenderPeriod.model_class()
        now = get_now()
        self.tenderPeriod.startDate = self.enquiryPeriod.startDate = now
        self.enquiryPeriod.endDate = self.tenderPeriod.endDate = calculate_business_date(self.auctionPeriod.startDate, DUTCH_PERIOD + AUCTION_START, self)
        self.auctionPeriod.startDate = None
        self.auctionPeriod.endDate = None
        self.date = now
        if self.lots:
            for lot in self.lots:
                lot.date = now
        self.documents.append(type(self).documents.model_class(DGF_PLATFORM_LEGAL_DETAILS))

DGFInsider = Auction

