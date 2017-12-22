# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.insider.tests.base import (
    BaseInsiderAuctionWebTest, test_financial_bids,
    test_insider_auction_data, test_financial_organization,
)
from openprocurement.auctions.core.tests.base import snitch
from .blanks.bidder import (
    # InsiderAuctionBidderResourceTest
    create_auction_bidder_invalid,
    create_auction_bidder,
    create_auction_bidder_without_value,
    patch_auction_bidder,
    get_auction_bidder,
    bid_id_signature_verified_active_bid,
    bid_id_signature_verified_draft_active_bid,
    delete_auction_bidder,
    get_auction_auctioners,
    bid_Administrator_change,
    # InsiderAuctionBidderDocumentResourceTest
    not_found,
    create_auction_bidder_document,
    put_auction_bidder_document,
    patch_auction_bidder_document,
    create_auction_bidder_document_nopending,
    # InsiderAuctionBidderDocumentWithDSResourceTest
    create_auction_bidder_document_json,
    put_auction_bidder_document_json
)


class InsiderAuctionBidderResourceTest(BaseInsiderAuctionWebTest):
    initial_status = 'active.tendering'
    test_financial_organization = test_financial_organization

    test_create_auction_bidder_invalid = snitch(create_auction_bidder_invalid)
    test_create_auction_bidder = snitch(create_auction_bidder)
    test_create_auction_bidder_without_value = snitch(create_auction_bidder_without_value)
    test_patch_auction_bidder = snitch(patch_auction_bidder)
    test_get_auction_bidder = snitch(get_auction_bidder)
    test_bid_id_signature_verified_active_bid = snitch(bid_id_signature_verified_active_bid)
    test_bid_id_signature_verified_draft_active_bid = snitch(bid_id_signature_verified_draft_active_bid)
    test_delete_auction_bidder = snitch(delete_auction_bidder)
    test_get_auction_auctioners = snitch(get_auction_auctioners)
    test_bid_Administrator_change = snitch(bid_Administrator_change)


class InsiderAuctionBidderDocumentResourceTest(BaseInsiderAuctionWebTest):
    initial_status = 'active.tendering'

    def setUp(self):
        super(InsiderAuctionBidderDocumentResourceTest, self).setUp()
        # Create bid
        response = self.app.post_json('/auctions/{}/bids'.format(
            self.auction_id), {'data': {'tenderers': [self.initial_organization], 'qualified': True, 'eligible': True}})
        bid = response.json['data']
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']

    test_not_found = snitch(not_found)
    test_create_auction_bidder_document = snitch(create_auction_bidder_document)
    test_put_auction_bidder_document = snitch(put_auction_bidder_document)
    test_patch_auction_bidder_document = snitch(patch_auction_bidder_document)
    test_create_auction_bidder_document_nopending = snitch(create_auction_bidder_document_nopending)


class InsiderAuctionBidderDocumentWithDSResourceTest(InsiderAuctionBidderDocumentResourceTest):
    docservice = True

    test_create_auction_bidder_document_json = snitch(create_auction_bidder_document_json)
    test_put_auction_bidder_document_json = snitch(put_auction_bidder_document_json)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InsiderAuctionBidderResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionBidderDocumentResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionBidderDocumentWithDSResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
