# -*- coding: utf-8 -*-
from schematics.types import StringType
from schematics.types.compound import ModelType
from schematics.exceptions import ValidationError
from schematics.transforms import  whitelist
from schematics.types.serializable import serializable
from zope.interface import implementer
from openprocurement.api.models import (
    Model, ListType
)
from openprocurement.auctions.core.models import IAuction
from openprocurement.auctions.dgf.models import (
    DGFFinancialAssets as BaseAuction,
    get_auction, Bid as BaseBid,
    Organization
)

from urllib import quote
from base64 import b64encode


class Bid(BaseBid):
    tenderers = ListType(ModelType(Organization), required=True, min_size=1, max_size=1)

    class Options:
        roles = {
            'create': whitelist('tenderers', 'parameters', 'lotValues', 'status', 'qualified', 'eligible'),
        }

    def validate_participationUrl(self, data, url):
        if url and isinstance(data['__parent__'], Model) and get_auction(data['__parent__']).lots:
            raise ValidationError(u"url should be posted for each lot of bid")

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
        root = self.__parent__
        auction_id = root.id
        bidder_id = self.id
        parents = []
        while root.__parent__ is not None:
            parents[0:0] = [root]
            root = root.__parent__
        request = root.request
        auction_url = request.registry.auction_module_url
        signature = quote(b64encode(request.registry.signer.signature(bidder_id)))
        participation_url = '{}/auctions/{}/login?bidder_id={}&signature={}'.format(auction_url, auction_id, bidder_id, signature)
        if not self.participationUrl:
            return participation_url

@implementer(IAuction)
class Auction(BaseAuction):
    """Data regarding auction process - publicly inviting prospective contractors to submit bids for evaluation and selecting a winner or winners."""
    procurementMethodType = StringType(default="dgfInsider")
    bids = ListType(ModelType(Bid), default=list())  # A list of all the companies who entered submissions for the auction.



DGFInsider = Auction

