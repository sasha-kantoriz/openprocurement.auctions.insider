# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.insider.tests.base import (
    BaseInsiderAuctionWebTest, test_financial_bids,
    test_insider_auction_data, test_financial_organization,
)
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.insider.tests.blanks.complaint_blanks import (
    # InsiderAuctionComplaintResourceTest
    create_auction_complaint_invalid,
    create_auction_complaint,
    patch_auction_complaint,
    review_auction_complaint,
    get_auction_complaint,
    get_auction_complaints,
    # InsiderAuctionComplaintDocumentResourceTest
    not_found,
    create_auction_complaint_document,
    put_auction_complaint_document,
    patch_auction_complaint_document
)


class InsiderAuctionComplaintResourceTest(BaseInsiderAuctionWebTest):

    test_create_auction_complaint_invalid = snitch(create_auction_complaint_invalid)
    test_create_auction_complaint = snitch(create_auction_complaint)
    test_patch_auction_complaint = snitch(patch_auction_complaint)
    test_review_auction_complaint = snitch(review_auction_complaint)
    test_get_auction_complaint = snitch(get_auction_complaint)
    test_get_auction_complaints = snitch(get_auction_complaints)


class InsiderAuctionComplaintDocumentResourceTest(BaseInsiderAuctionWebTest):

    def setUp(self):
        super(InsiderAuctionComplaintDocumentResourceTest, self).setUp()
        # Create complaint
        response = self.app.post_json('/auctions/{}/complaints'.format(
            self.auction_id), {'data': {'title': 'complaint title', 'description': 'complaint description', 'author': self.initial_organization}})
        complaint = response.json['data']
        self.complaint_id = complaint['id']
        self.complaint_owner_token = response.json['access']['token']

    test_not_found = snitch(not_found)
    test_create_auction_complaint_document = snitch(create_auction_complaint_document)
    test_put_auction_complaint_document = snitch(put_auction_complaint_document)
    test_patch_auction_complaint_document = snitch(patch_auction_complaint_document)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InsiderAuctionComplaintDocumentResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionComplaintResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
