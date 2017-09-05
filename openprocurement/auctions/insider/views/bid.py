# -*- coding: utf-8 -*-

from openprocurement.auctions.core.utils import (
    opresource,
    save_auction,
)
from openprocurement.auctions.dgf.views.financial.bid import (
    FinancialAuctionBidResource,
)
from openprocurement.api.utils import (
    json_view,
    context_unpack
)
from openprocurement.api.models import get_now

@opresource(name='dgfInsider:Auction Bids',
            collection_path='/auctions/{auction_id}/bids',
            path='/auctions/{auction_id}/bids/{bid_id}',
            auctionsprocurementMethodType="dgfInsider",
            description="Insider auction bids")
class InsiderAuctionBidResource(FinancialAuctionBidResource):
    @json_view(permission='delete_bid')
    def delete(self):
        """Cancelling the proposal

        Example request for cancelling the proposal:

        .. sourcecode:: http

            DELETE /auctions/4879d3f8ee2443169b5fbbc9f89fa607/bids/71b6c23ed8944d688e92a31ec8c3f61a HTTP/1.1
            Host: example.com
            Accept: application/json

        And here is the response to be expected:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            {
                "data": {
                    "value": {
                        "amount": 489,
                        "currency": "UAH",
                        "valueAddedTaxIncluded": true
                    }
                }
            }

        """
        # Delete bid permission where deny for everyone
        # For return possibility delete bid remove this function
        bid = self.request.context
        if self.request.validated['auction_status'] != 'active.tendering':
            self.request.errors.add('body', 'data', 'Can\'t delete bid in current ({}) auction status'.format(self.request.validated['auction_status']))
            self.request.errors.status = 403
            return
        auction = self.request.validated['auction']
        if auction.tenderPeriod.startDate and get_now() < auction.tenderPeriod.startDate or get_now() > auction.tenderPeriod.endDate:
            self.request.errors.add('body', 'data', 'Bid can be deleted only during the tendering period: from ({}) to ({}).'.format(auction.tenderPeriod.startDate and auction.tenderPeriod.startDate.isoformat(), auction.tenderPeriod.endDate.isoformat()))
            self.request.errors.status = 403
            return
        res = bid.serialize("view")
        self.request.validated['auction'].bids.remove(bid)
        self.request.validated['auction'].modified = False
        if save_auction(self.request):
            self.LOGGER.info('Deleted auction bid {}'.format(self.request.context.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'auction_bid_delete'}))
            return {'data': res}

