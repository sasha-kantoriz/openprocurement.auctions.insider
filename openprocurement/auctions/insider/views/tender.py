# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.dgf.views.financial.tender import (
    FinancialAuctionResource,
)


@opresource(name='dgfInsider:Auction',
            path='/auctions/{auction_id}',
            auctionsprocurementMethodType="dgfInsider",
            description="Open Contracting compatible data exchange format. See http://ocds.open-contracting.org/standard/r/master/#auction for more info")
class InsiderAuctionResource(FinancialAuctionResource):
    pass
