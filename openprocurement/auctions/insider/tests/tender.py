# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.dgf.constants import ELIGIBILITY_CRITERIA
from openprocurement.auctions.insider.models import DGFInsider
from openprocurement.auctions.insider.tests.base import (
    test_insider_auction_data, test_insider_auction_data,
    test_organization, test_financial_organization,
    BaseInsiderAuctionWebTest, BaseInsiderWebTest,
)
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.insider.tests.blanks.tender_blanks import (
    # InsiderAuctionTest
    simple_add_auction,
    create_role,
    edit_role,
    # InsiderAuctionResourceTest
    empty_listing,
    listing,
    listing_changes,
    listing_draft,
    create_auction_invalid,
    create_auction_auctionPeriod,
    create_auction_generated,
    create_auction_draft,
    create_auction,
    get_auction,
    patch_auction,
    dateModified_auction,
    auction_not_found,
    guarantee,
    auction_Administrator_change,
    # InsiderAuctionProcessTest
    one_valid_bid_auction,
    one_invalid_bid_auction,
    first_bid_auction,
    auctionUrl_in_active_auction,
    suspended_auction
)


class InsiderAuctionTest(BaseInsiderWebTest):
    auction = DGFInsider
    initial_data = test_insider_auction_data

    test_simple_add_auction = snitch(simple_add_auction)
    test_create_role = snitch(create_role)
    test_edit_role = snitch(edit_role)


class InsiderAuctionResourceTest(BaseInsiderWebTest):
    initial_data = test_insider_auction_data
    initial_organization = test_organization
    eligibility_criteria = ELIGIBILITY_CRITERIA
    test_financial_organization = test_financial_organization

    test_empty_listing = snitch(empty_listing)
    test_listing = snitch(listing)
    test_listing_changes = snitch(listing_changes)
    test_listing_draft = snitch(listing_draft)
    test_create_auction_invalid = snitch(create_auction_invalid)
    test_create_auction_auctionPeriod = snitch(create_auction_auctionPeriod)
    test_create_auction_generated = snitch(create_auction_generated)
    test_create_auction_draft = snitch(create_auction_draft)
    test_create_auction = snitch(create_auction)
    test_get_auction = snitch(get_auction)
    test_patch_auction = snitch(patch_auction)
    test_dateModified_auction = snitch(dateModified_auction)
    test_auction_not_found = snitch(auction_not_found)
    test_guarantee = snitch(guarantee)
    test_auction_Administrator_change = snitch(auction_Administrator_change)


class InsiderAuctionProcessTest(BaseInsiderAuctionWebTest):

    test_financial_organization = test_financial_organization

    #setUp = BaseInsiderWebTest.setUp
    def setUp(self):
        super(InsiderAuctionProcessTest.__bases__[0], self).setUp()

    test_one_valid_bid_auction = unittest.skip(snitch(one_valid_bid_auction))
    test_one_invalid_bid_auction = unittest.skip(snitch(one_invalid_bid_auction))
    test_first_bid_auction = snitch(first_bid_auction)
    test_auctionUrl_in_active_auction = snitch(auctionUrl_in_active_auction)
    test_suspended_auction = snitch(suspended_auction)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InsiderAuctionProcessTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
