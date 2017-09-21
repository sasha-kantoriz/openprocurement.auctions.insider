# -*- coding: utf-8 -*-
import unittest
from datetime import timedelta
from openprocurement.api.models import get_now
from openprocurement.auctions.insider.tests.base import (
    BaseInsiderAuctionWebTest, test_financial_bids,
    test_insider_auction_data, test_financial_organization,
)


class InsiderAuctionSwitchQualificationResourceTest(BaseInsiderAuctionWebTest):
    initial_bids = test_financial_bids[:1]

    def test_switch_to_qualification(self):
        response = self.set_status('active.auction', {'status': self.initial_status})
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "unsuccessful")
        self.assertNotIn("awards", response.json['data'])


class InsiderAuctionSwitchAuctionResourceTest(BaseInsiderAuctionWebTest):
    initial_bids = test_financial_bids

    @unittest.skip("DUTCH")
    def test_switch_to_auction(self):
        response = self.set_status('active.auction', {'status': self.initial_status})
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "active.auction")

    # DUTCH
    def test_switch_to_unsuccessful(self):
        response = self.set_status('active.auction', {'status': self.initial_status})
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "unsuccessful")


class InsiderAuctionSwitchUnsuccessfulResourceTest(BaseInsiderAuctionWebTest):

    def test_switch_to_unsuccessful(self):
        response = self.set_status('active.auction', {'status': self.initial_status})
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "unsuccessful")
        if self.initial_lots:
            self.assertEqual(set([i['status'] for i in response.json['data']["lots"]]), set(["unsuccessful"]))


class InsiderAuctionAuctionPeriodResourceTest(BaseInsiderAuctionWebTest):
    initial_bids = test_financial_bids

    def test_set_auction_period(self):
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], 'active.tendering')
        if self.initial_lots:
            item = response.json['data']["lots"][0]
        else:
            item = response.json['data']
        self.assertIn('auctionPeriod', item)
        self.assertIn('shouldStartAfter', item['auctionPeriod'])
        self.assertGreaterEqual(response.json['data']['tenderPeriod']['endDate'], item['auctionPeriod']['shouldStartAfter'])
        self.assertIn('T00:00:00+', item['auctionPeriod']['shouldStartAfter'])
        self.assertEqual(response.json['data']['next_check'], response.json['data']['tenderPeriod']['endDate'])

        if self.initial_lots:
            response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"lots": [{"auctionPeriod": {"startDate": "9999-01-01T00:00:00+00:00"}}]}})
            item = response.json['data']["lots"][0]
        else:
            response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"auctionPeriod": {"startDate": "9999-01-01T00:00:00+00:00"}}})
            item = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(item['auctionPeriod']['startDate'], '9999-01-01T00:00:00+00:00')

        if self.initial_lots:
            response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"lots": [{"auctionPeriod": {"startDate": None}}]}})
            item = response.json['data']["lots"][0]
        else:
            response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"auctionPeriod": {"startDate": None}}})
            item = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertNotIn('startDate', item['auctionPeriod'])

    def test_reset_auction_period(self):
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], 'active.tendering')
        if self.initial_lots:
            item = response.json['data']["lots"][0]
        else:
            item = response.json['data']
        self.assertIn('auctionPeriod', item)
        self.assertIn('shouldStartAfter', item['auctionPeriod'])
        self.assertGreaterEqual(response.json['data']['tenderPeriod']['endDate'], item['auctionPeriod']['shouldStartAfter'])
        self.assertEqual(response.json['data']['next_check'], response.json['data']['tenderPeriod']['endDate'])

        if self.initial_lots:
            response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"lots": [{"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}]}})
            item = response.json['data']["lots"][0]
        else:
            response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}})
            item = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertGreaterEqual(response.json['data']['tenderPeriod']['endDate'], item['auctionPeriod']['shouldStartAfter'])
        self.assertIn('9999-01-01T00:00:00', item['auctionPeriod']['startDate'])

        self.set_status('active.auction', {'status': 'active.tendering'})
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']["status"], 'unsuccessful')
        #DUTCH
        # item = response.json['data']["lots"][0] if self.initial_lots else response.json['data']
        # self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'], response.json['data']['tenderPeriod']['endDate'])
        #
        # if self.initial_lots:
        #     response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"lots": [{"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}]}})
        #     item = response.json['data']["lots"][0]
        # else:
        #     response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}})
        #     item = response.json['data']
        # self.assertEqual(response.status, '200 OK')
        # self.assertEqual(response.json['data']["status"], 'active.auction')
        # self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'], response.json['data']['tenderPeriod']['endDate'])
        # self.assertIn('9999-01-01T00:00:00', item['auctionPeriod']['startDate'])
        # self.assertIn('9999-01-01T00:00:00', response.json['data']['next_check'])
        #
        # now = get_now().isoformat()
        # auction = self.db.get(self.auction_id)
        # if self.initial_lots:
        #     auction['lots'][0]['auctionPeriod']['startDate'] = now
        # else:
        #     auction['auctionPeriod']['startDate'] = now
        # self.db.save(auction)
        #
        # response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        # self.assertEqual(response.status, '200 OK')
        # self.assertEqual(response.json['data']["status"], 'active.auction')
        # item = response.json['data']["lots"][0] if self.initial_lots else response.json['data']
        # self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'], response.json['data']['tenderPeriod']['endDate'])
        # self.assertGreater(response.json['data']['next_check'], item['auctionPeriod']['startDate'])
        # self.assertEqual(response.json['data']['next_check'], self.db.get(self.auction_id)['next_check'])
        #
        # if self.initial_lots:
        #     response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"lots": [{"auctionPeriod": {"startDate": response.json['data']['tenderPeriod']['endDate']}}]}})
        #     item = response.json['data']["lots"][0]
        # else:
        #     response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"auctionPeriod": {"startDate": response.json['data']['tenderPeriod']['endDate']}}})
        #     item = response.json['data']
        # self.assertEqual(response.status, '200 OK')
        # self.assertEqual(response.json['data']["status"], 'active.auction')
        # self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'], response.json['data']['tenderPeriod']['endDate'])
        # self.assertNotIn('9999-01-01T00:00:00', item['auctionPeriod']['startDate'])
        # self.assertGreater(response.json['data']['next_check'], response.json['data']['tenderPeriod']['endDate'])
        #
        # auction = self.db.get(self.auction_id)
        # self.assertGreater(auction['next_check'], response.json['data']['tenderPeriod']['endDate'])
        # auction['tenderPeriod']['endDate'] = auction['tenderPeriod']['startDate']
        # if self.initial_lots:
        #     auction['lots'][0]['auctionPeriod']['startDate'] = auction['tenderPeriod']['startDate']
        # else:
        #     auction['auctionPeriod']['startDate'] = auction['tenderPeriod']['startDate']
        # self.db.save(auction)
        #
        # response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        # if self.initial_lots:
        #     item = response.json['data']["lots"][0]
        # else:
        #     item = response.json['data']
        # self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'], response.json['data']['tenderPeriod']['endDate'])
        # self.assertNotIn('next_check', response.json['data'])
        # self.assertNotIn('next_check', self.db.get(self.auction_id))
        # shouldStartAfter = item['auctionPeriod']['shouldStartAfter']
        #
        # response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        # if self.initial_lots:
        #     item = response.json['data']["lots"][0]
        # else:
        #     item = response.json['data']
        # self.assertEqual(item['auctionPeriod']['shouldStartAfter'], shouldStartAfter)
        # self.assertNotIn('next_check', response.json['data'])
        #
        # if self.initial_lots:
        #     response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"lots": [{"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}]}})
        #     item = response.json['data']["lots"][0]
        # else:
        #     response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}})
        #     item = response.json['data']
        # self.assertEqual(response.status, '200 OK')
        # self.assertEqual(response.json['data']["status"], 'active.auction')
        # self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'], response.json['data']['tenderPeriod']['endDate'])
        # self.assertIn('9999-01-01T00:00:00', item['auctionPeriod']['startDate'])
        # self.assertIn('9999-01-01T00:00:00', response.json['data']['next_check'])


class InsiderAuctionAwardSwitchResourceTest(BaseInsiderAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = test_financial_bids

    def setUp(self):
        super(InsiderAuctionAwardSwitchResourceTest, self).setUp()
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
        self.award = self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.award_id = self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization

    def test_switch_verification_to_unsuccessful(self):
        auction = self.db.get(self.auction_id)
        auction['awards'][0]['verificationPeriod']['endDate'] = auction['awards'][0]['verificationPeriod']['startDate']
        self.db.save(auction)

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'unsuccessful')
        self.assertEqual(auction['awards'][1]['status'], 'pending.verification')
        self.assertEqual(auction['status'], 'active.qualification')
        self.assertNotIn('endDate', auction['awardPeriod'])

    def test_switch_payment_to_unsuccessful(self):
        bid_token = self.initial_bids_tokens[self.award['bid_id']]
        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, self.award_id, doc_id, self.auction_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')

        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "pending.payment"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "pending.payment")

        auction = self.db.get(self.auction_id)
        auction['awards'][0]['paymentPeriod']['endDate'] = auction['awards'][0]['paymentPeriod']['startDate']
        self.db.save(auction)

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'unsuccessful')
        self.assertEqual(auction['awards'][1]['status'], 'pending.verification')
        self.assertEqual(auction['status'], 'active.qualification')
        self.assertNotIn('endDate', auction['awardPeriod'])

    def test_switch_active_to_unsuccessful(self):
        bid_token = self.initial_bids_tokens[self.award['bid_id']]
        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, self.award_id, doc_id, self.auction_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')

        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "pending.payment"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "pending.payment")

        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "active"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "active")

        auction = self.db.get(self.auction_id)
        auction['awards'][0]['signingPeriod']['endDate'] = auction['awards'][0]['signingPeriod']['startDate']
        self.db.save(auction)

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'unsuccessful')
        self.assertEqual(auction['contracts'][0]['status'], 'cancelled')
        self.assertEqual(auction['awards'][1]['status'], 'pending.verification')
        self.assertEqual(auction['status'], 'active.qualification')
        self.assertNotIn('endDate', auction['awardPeriod'])


class InsiderAuctionAwardSwitch2ResourceTest(BaseInsiderAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = test_financial_bids

    def setUp(self):
        super(InsiderAuctionAwardSwitch2ResourceTest, self).setUp()
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('auction', ''))

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
                    "value": {"amount": 101 * (i + 1)},

                }
                for i, b in enumerate(self.initial_bids)
            ]
        }

        response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': auction_result})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']
        self.assertEqual('active.qualification', auction["status"])
        self.award = self.first_award = auction['awards'][0]
        # self.second_award = auction['awards'][1]
        self.award_id = self.first_award_id = self.first_award['id']
        # self.second_award_id = self.second_award['id']
        self.app.authorization = authorization

    def test_switch_verification_to_unsuccessful(self):
        auction = self.db.get(self.auction_id)
        auction['awards'][0]['verificationPeriod']['endDate'] = auction['awards'][0]['verificationPeriod']['startDate']
        self.db.save(auction)

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'unsuccessful')
        # self.assertEqual(auction['awards'][1]['status'], 'unsuccessful')
        # self.assertEqual(auction['status'], 'unsuccessful')
        # self.assertIn('endDate', auction['awardPeriod'])

    def test_switch_payment_to_unsuccessful(self):
        bid_token = self.initial_bids_tokens[self.award['bid_id']]
        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, self.award_id, doc_id, self.auction_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')

        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "pending.payment"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "pending.payment")

        auction = self.db.get(self.auction_id)
        auction['awards'][0]['paymentPeriod']['endDate'] = auction['awards'][0]['paymentPeriod']['startDate']
        self.db.save(auction)

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'unsuccessful')
        # self.assertEqual(auction['awards'][1]['status'], 'unsuccessful')
        # self.assertEqual(auction['status'], 'unsuccessful')
        # self.assertIn('endDate', auction['awardPeriod'])

    def test_switch_active_to_unsuccessful(self):
        bid_token = self.initial_bids_tokens[self.award['bid_id']]
        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, self.award_id, doc_id, self.auction_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')

        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "pending.payment"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "pending.payment")

        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "active"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "active")

        auction = self.db.get(self.auction_id)
        auction['awards'][0]['signingPeriod']['endDate'] = auction['awards'][0]['signingPeriod']['startDate']
        self.db.save(auction)

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'unsuccessful')
        self.assertEqual(auction['contracts'][0]['status'], 'cancelled')
        # self.assertEqual(auction['awards'][1]['status'], 'unsuccessful')
        # self.assertEqual(auction['status'], 'unsuccessful')
        # self.assertIn('endDate', auction['awardPeriod'])


class InsiderAuctionDontSwitchSuspendedAuction2ResourceTest(BaseInsiderAuctionWebTest):
    initial_bids = test_financial_bids

    def test_switch_suspended_auction_to_auction(self):
        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'suspended': True}})
        response = self.set_status('active.auction', {'status': self.initial_status})

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertNotEqual(response.json['data']["status"], "active.auction")

        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'suspended': False}})

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')

        self.assertEqual(response.json['data']["status"], "unsuccessful")
        # Dutch
        # self.assertEqual(response.json['data']["status"], "active.auction")


class InsiderAuctionDontSwitchSuspendedAuctionResourceTest(BaseInsiderAuctionWebTest):
    initial_status = 'active.auction'
    initial_bids = test_financial_bids

    def setUp(self):
        super(InsiderAuctionDontSwitchSuspendedAuctionResourceTest, self).setUp()
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
        self.award = self.first_award = auction['awards'][0]
        self.second_award = auction['awards'][1]
        self.award_id = self.first_award_id = self.first_award['id']
        self.second_award_id = self.second_award['id']
        self.app.authorization = authorization

    def test_switch_suspended_verification_to_unsuccessful(self):
        auction = self.db.get(self.auction_id)
        auction['awards'][0]['verificationPeriod']['endDate'] = auction['awards'][0]['verificationPeriod']['startDate']
        self.db.save(auction)

        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'suspended': True}})

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'pending.verification')
        self.assertEqual(auction['awards'][1]['status'], 'pending.waiting')

        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'suspended': False}})

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'unsuccessful')
        self.assertEqual(auction['awards'][1]['status'], 'pending.verification')
        self.assertEqual(auction['status'], 'active.qualification')
        self.assertNotIn('endDate', auction['awardPeriod'])

    def test_switch_suspended_payment_to_unsuccessful(self):
        bid_token = self.initial_bids_tokens[self.award['bid_id']]
        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, self.award_id, doc_id, self.auction_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')

        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "pending.payment"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "pending.payment")

        auction = self.db.get(self.auction_id)
        auction['awards'][0]['paymentPeriod']['endDate'] = auction['awards'][0]['paymentPeriod']['startDate']
        self.db.save(auction)

        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'suspended': True}})

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'pending.payment')
        self.assertEqual(auction['awards'][1]['status'], 'pending.waiting')

        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'suspended': False}})

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'unsuccessful')
        self.assertEqual(auction['awards'][1]['status'], 'pending.verification')
        self.assertEqual(auction['status'], 'active.qualification')
        self.assertNotIn('endDate', auction['awardPeriod'])

    def test_switch_suspended_active_to_unsuccessful(self):
        bid_token = self.initial_bids_tokens[self.award['bid_id']]
        response = self.app.post('/auctions/{}/awards/{}/documents?acc_token={}'.format(
            self.auction_id, self.award_id, self.auction_token), upload_files=[('file', 'auction_protocol.pdf', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.patch_json('/auctions/{}/awards/{}/documents/{}?acc_token={}'.format(self.auction_id, self.award_id, doc_id, self.auction_token), {"data": {
            "description": "auction protocol",
            "documentType": 'auctionProtocol'
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json["data"]["documentType"], 'auctionProtocol')

        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "pending.payment"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "pending.payment")

        response = self.app.patch_json('/auctions/{}/awards/{}'.format(self.auction_id, self.award_id), {"data": {"status": "active"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "active")

        auction = self.db.get(self.auction_id)
        auction['awards'][0]['signingPeriod']['endDate'] = auction['awards'][0]['signingPeriod']['startDate']
        self.db.save(auction)

        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'suspended': True}})

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        self.assertEqual(response.status, '200 OK')
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'active')
        self.assertEqual(auction['contracts'][0]['status'], 'pending')
        self.assertEqual(auction['awards'][1]['status'], 'pending.waiting')
        self.assertEqual(auction['status'], 'active.awarded')
        self.assertIn('endDate', auction['awardPeriod'])

        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'suspended': False}})

        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
        auction = response.json['data']
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(auction['awards'][0]['status'], 'unsuccessful')
        self.assertEqual(auction['contracts'][0]['status'], 'cancelled')
        self.assertEqual(auction['awards'][1]['status'], 'pending.verification')
        self.assertEqual(auction['status'], 'active.qualification')
        self.assertNotIn('endDate', auction['awardPeriod'])



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InsiderAuctionSwitchQualificationResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionSwitchAuctionResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionSwitchUnsuccessfulResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionAuctionPeriodResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionAwardSwitchResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionAwardSwitchResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionAwardSwitch2ResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionComplaintSwitchResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionDontSwitchSuspendedAuction2ResourceTest))
    suite.addTest(unittest.makeSuite(InsiderAuctionDontSwitchSuspendedAuctionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
