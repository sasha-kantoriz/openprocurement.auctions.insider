# -*- coding: utf-8 -*-
import unittest

from openprocurement.auctions.dgf.models import DGF_PLATFORM_LEGAL_DETAILS_FROM
from openprocurement.auctions.insider.tests.base import BaseInsiderAuctionWebTest
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.insider.tests.blanks.document_blanks import (
    # InsiderAuctionDocumentResourceTest
    not_found,
    create_auction_document,
    put_auction_document,
    patch_auction_document,
    # InsiderAuctionDocumentWithDSResourceTest
    create_auction_document_json_invalid,
    create_auction_document_json,
    put_auction_document_json,
    create_auction_document_pas,
    put_auction_document_pas,
    create_auction_offline_document,
    put_auction_offline_document,
    create_auction_document_vdr,
    put_auction_document_vdr,
)


class InsiderAuctionDocumentResourceTest(BaseInsiderAuctionWebTest):
    docservice = False
    dgf_platform_legal_details_from = DGF_PLATFORM_LEGAL_DETAILS_FROM

    test_not_found = snitch(not_found)
    test_create_auction_document = snitch(create_auction_document)
    test_put_auction_document = snitch(put_auction_document)
    test_patch_auction_document = snitch(patch_auction_document)


class InsiderAuctionDocumentWithDSResourceTest(InsiderAuctionDocumentResourceTest):
    docservice = True

    test_create_auction_document_json_invalid = snitch(create_auction_document_json_invalid)
    test_create_auction_document_json = snitch(create_auction_document_json)
    test_put_auction_document_json = snitch(put_auction_document_json)
    test_create_auction_document_pas = snitch(create_auction_document_pas)
    test_put_auction_document_pas = snitch(put_auction_document_pas)
    test_create_auction_offline_document = snitch(create_auction_offline_document)
    test_put_auction_offline_document = snitch(put_auction_offline_document)
    test_create_auction_document_vdr = snitch(create_auction_document_vdr)
    test_put_auction_document_vdr = snitch(put_auction_document_vdr)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InsiderAuctionDocumentResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionDocumentWithDSResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
