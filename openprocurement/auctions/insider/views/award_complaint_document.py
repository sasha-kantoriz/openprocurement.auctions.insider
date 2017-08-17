# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.dgf.views.financial.award_complaint_document import (
    FinancialAuctionAwardComplaintDocumentResource,
)


@opresource(name='dgfInsider:Auction Award Complaint Documents',
            collection_path='/auctions/{auction_id}/awards/{award_id}/complaints/{complaint_id}/documents',
            path='/auctions/{auction_id}/awards/{award_id}/complaints/{complaint_id}/documents/{document_id}',
            auctionsprocurementMethodType="dgfInsider",
            description="Insider auction award complaint documents")
class InsiderAuctionAwardComplaintDocumentResource(FinancialAuctionAwardComplaintDocumentResource):
    pass