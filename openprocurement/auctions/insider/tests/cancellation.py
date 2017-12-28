# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.insider.tests.base import (
    BaseInsiderAuctionWebTest, test_financial_bids,
    test_insider_auction_data, test_financial_organization,
)
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.insider.tests.blanks.cancellation_blanks import (
    # InsiderAuctionCancellationResourceTest
    create_auction_cancellation_invalid,
    create_auction_cancellation,
    patch_auction_cancellation,
    get_auction_cancellation,
    get_auction_cancellations,
    # InsiderAuctionCancellationDocumentResourceTest
    not_found,
    create_auction_cancellation_document,
    put_auction_cancellation_document,
    patch_auction_cancellation_document
)


class InsiderAuctionCancellationResourceTest(BaseInsiderAuctionWebTest):
    initial_status = 'active.tendering'
    initial_bids = test_financial_bids

    test_create_auction_cancellation_invalid = snitch(create_auction_cancellation_invalid)
    test_create_auction_cancellation = snitch(create_auction_cancellation)
    test_patch_auction_cancellation = snitch(patch_auction_cancellation)
    test_get_auction_cancellation = snitch(get_auction_cancellation)
    test_get_auction_cancellations = snitch(get_auction_cancellations)


class InsiderAuctionCancellationDocumentResourceTest(BaseInsiderAuctionWebTest):

    def setUp(self):
        super(InsiderAuctionCancellationDocumentResourceTest, self).setUp()
        # Create cancellation
        response = self.app.post_json('/auctions/{}/cancellations'.format(
            self.auction_id), {'data': {'reason': 'cancellation reason'}})
        cancellation = response.json['data']
        self.cancellation_id = cancellation['id']

    test_not_found = snitch(not_found)
    test_create_auction_cancellation_document = snitch(create_auction_cancellation_document)
    test_put_auction_cancellation_document = snitch(put_auction_cancellation_document)
    test_patch_auction_cancellation_document = snitch(patch_auction_cancellation_document)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InsiderAuctionCancellationResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionCancellationDocumentResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
