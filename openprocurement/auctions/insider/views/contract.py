# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.dgf.views.financial.contract import (
    FinancialAuctionAwardContractResource,
)


@opresource(name='dgfInsider:Auction Contracts',
            collection_path='/auctions/{auction_id}/contracts',
            path='/auctions/{auction_id}/contracts/{contract_id}',
            auctionsprocurementMethodType="dgfInsider",
            description="Insider auction contracts")
class InsiderAuctionAwardContractResource(FinancialAuctionAwardContractResource):
    pass
