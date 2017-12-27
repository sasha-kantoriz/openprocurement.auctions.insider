# -*- coding: utf-8 -*-
import unittest
from datetime import timedelta

from openprocurement.api.models import get_now
from openprocurement.auctions.insider.tests.base import (
    BaseInsiderAuctionWebTest, test_financial_bids,
    test_insider_auction_data, test_financial_organization,
)
from openprocurement.auctions.core.tests.base import snitch
from openprocurement.auctions.insider.tests.blanks.award_blanks import (
    # InsiderAuctionCreateAwardTest
    create_auction_award_invalid,
    create_auction_award,
    # InsiderAuctionAwardProcessTest
    invalid_patch_auction_award,
    patch_auction_award,
    patch_auction_award_admin,
    complate_auction_with_second_award1,
    complate_auction_with_second_award2,
    complate_auction_with_second_award3,
    successful_second_auction_award,
    unsuccessful_auction1,
    unsuccessful_auction2,
    unsuccessful_auction3,
    unsuccessful_auction4,
    unsuccessful_auction5,
    get_auction_awards,
    # InsiderAuctionAwardDocumentResourceTest
    not_found,
    create_auction_award_document,
    put_auction_award_document,
    patch_auction_award_document
)


class InsiderAuctionCreateAwardTest(BaseInsiderAuctionWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_financial_bids

    test_create_auction_award_invalid = snitch(create_auction_award_invalid)
    test_create_auction_award = snitch(create_auction_award)


class InsiderAuctionAwardProcessTest(BaseInsiderAuctionWebTest):
    #initial_data = auction_data
    initial_status = 'active.auction'
    initial_bids = test_financial_bids

    def upload_auction_protocol(self, award):
        award_id = award['id']
        bid_token = self.initial_bids_tokens[award['bid_id']]
        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, award_id, bid_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('auction_protocol.pdf', response.json["data"]["title"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, award_id, doc_id, bid_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertIn("documentType", response.json["data"])
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')

        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('auction_protocol.pdf', response.json["data"]["title"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.patch_json(
            '/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, award_id, doc_id, self.auction_token),
            {"data": {
                "description": "auction protocol",
                "documentType": 'auctionProtocol'
            }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertIn("documentType", response.json["data"])
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')

        response = self.app.get('/auctions/{}/awards/{}/documents'.format(self.auction_id,award_id, doc_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual('auctionProtocol', response.json["data"][0]["documentType"])
        self.assertEqual('auction_protocol.pdf', response.json["data"][0]["title"])
        self.assertEqual('bid_owner', response.json["data"][0]["author"])
        self.assertEqual('auctionProtocol', response.json["data"][1]["documentType"])
        self.assertEqual('auction_owner', response.json["data"][1]["author"])

    def setUp(self):
        super(InsiderAuctionAwardProcessTest, self).setUp()

        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))
        now = get_now()
        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

        now = get_now()
        auction_result = {
            'bids': [
                {
                    "id": b['id'],
                    "date": (now - timedelta(seconds=i)).isoformat(),
                    "value": {"amount": value_threshold * 2},

                }
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization

    test_invalid_patch_auction_award = snitch(invalid_patch_auction_award)
    test_patch_auction_award = snitch(patch_auction_award)
    test_patch_auction_award_admin = snitch(patch_auction_award_admin)
    test_complate_auction_with_second_award1 = snitch(complate_auction_with_second_award1)
    test_complate_auction_with_second_award2 = snitch(complate_auction_with_second_award2)
    test_complate_auction_with_second_award3 = snitch(complate_auction_with_second_award3)
    test_successful_second_auction_award = snitch(successful_second_auction_award)
    test_unsuccessful_auction1 = snitch(unsuccessful_auction1)
    test_unsuccessful_auction2 = snitch(unsuccessful_auction2)
    test_unsuccessful_auction3 = snitch(unsuccessful_auction3)
    test_unsuccessful_auction4 = snitch(unsuccessful_auction4)
    test_unsuccessful_auction5 = snitch(unsuccessful_auction5)
    test_get_auction_awards = snitch(get_auction_awards)


class InsiderAuctionAwardDocumentResourceTest(BaseInsiderAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = test_financial_bids

    def setUp(self):
        super(InsiderAuctionAwardDocumentResourceTest, self).setUp()
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))
        now = get_now()

        response = self.app.get('/auctions/{}'.format(self.auction_id))
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        value_threshold = auction['value']['amount'] + auction['minimalStep']['amount']

        now = get_now()
        auction_result = {
            'bids': [
                {
                    "id": b['id'],
                    "date": (now - timedelta(seconds=i)).isoformat(),
                    "value": {"amount": value_threshold * 2},

                }
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization

    test_not_found = snitch(not_found)
    test_create_auction_award_document = snitch(create_auction_award_document)
    test_put_auction_award_document = snitch(put_auction_award_document)
    test_patch_auction_award_document = snitch(patch_auction_award_document)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InsiderAuctionCreateAwardTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionAwardProcessTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionAwardDocumentResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
