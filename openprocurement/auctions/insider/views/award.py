# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.dgf.views.financial.award import (
    FinancialAuctionAwardResource,
)


@opresource(name='dgfInsider:Auction Awards',
            collection_path='/auctions/{auction_id}/awards',
            path='/auctions/{auction_id}/awards/{award_id}',
            auctionsprocurementMethodType="dgfInsider",
            description="Insider auction awards")
class InsiderAuctionAwardResource(FinancialAuctionAwardResource):
    pass
