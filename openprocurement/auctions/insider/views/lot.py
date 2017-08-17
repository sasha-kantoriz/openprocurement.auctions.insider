# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.dgf.views.financial.lot import (
    FinancialAuctionLotResource,
)


@opresource(name='dgfInsider:Auction Lots',
            collection_path='/auctions/{auction_id}/lots',
            path='/auctions/{auction_id}/lots/{lot_id}',
            auctionsprocurementMethodType="dgfInsider",
            description="Insider auction lots")
class InsiderAuctionLotResource(FinancialAuctionLotResource):
    pass
