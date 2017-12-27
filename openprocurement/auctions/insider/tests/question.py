# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.insider.tests.base import (
    BaseInsiderAuctionWebTest, test_financial_bids,
    test_insider_auction_data, test_financial_organization,
)
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.insider.tests.blanks.question_blanks import (
    # InsiderAuctionQuestionResourceTest
    create_auction_question_invalid,
    create_auction_question,
    patch_auction_question,
    get_auction_question,
    get_auction_questions
)


class InsiderAuctionQuestionResourceTest(BaseInsiderAuctionWebTest):

    test_create_auction_question_invalid = snitch(create_auction_question_invalid)
    test_create_auction_question = snitch(create_auction_question)
    test_patch_auction_question = snitch(patch_auction_question)
    test_get_auction_question = snitch(get_auction_question)
    test_get_auction_questions = snitch(get_auction_questions)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InsiderAuctionQuestionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
