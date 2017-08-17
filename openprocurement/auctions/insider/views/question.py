# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
)
from openprocurement.auctions.dgf.views.financial.question import (
    FinancialAuctionQuestionResource,
)


@opresource(name='dgfInsider:Auction Questions',
            collection_path='/auctions/{auction_id}/questions',
            path='/auctions/{auction_id}/questions/{question_id}',
            auctionsprocurementMethodType="dgfInsider",
            description="dgfInsider:Auction questions")
class InsiderAuctionQuestionResource(FinancialAuctionQuestionResource):
    pass
