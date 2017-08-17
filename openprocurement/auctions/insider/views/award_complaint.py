# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.dgf.views.financial.award_complaint import (
    FinancialAuctionAwardComplaintResource,
)

@opresource(name='dgfInsider:Auction Award Complaints',
            collection_path='/auctions/{auction_id}/awards/{award_id}/complaints',
            path='/auctions/{auction_id}/awards/{award_id}/complaints/{complaint_id}',
            auctionsprocurementMethodType="dgfInsider",
            description="Insider auction award complaints")
class InsiderAuctionAwardComplaintResource(FinancialAuctionAwardComplaintResource):
    pass