# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.dgf.views.financial.contract_document import (
    FinancialAuctionAwardContractDocumentResource,
)


@opresource(name='dgfInsider:Auction Contract Documents',
            collection_path='/auctions/{auction_id}/contracts/{contract_id}/documents',
            path='/auctions/{auction_id}/contracts/{contract_id}/documents/{document_id}',
            auctionsprocurementMethodType="dgfInsider",
            description="Insider auction contract documents")
class InsiderAuctionAwardContractDocumentResource(FinancialAuctionAwardContractDocumentResource):
    pass
