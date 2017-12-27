from openprocurement.api.models import get_now


# InsiderAuctionSwitchAuctionResourceTest
def switch_to_auction(self):
    response = self.set_status('active.auction', {'status': self.initial_status})
    self.app.authorization = ('Basic', ('chronograph', ''))
    response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["status"], "active.auction")


# InsiderAuctionAuctionPeriodResourceTest
def set_auction_period(self):
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
    self.assertGreaterEqual(response.json['data']['tenderPeriod']['endDate'],
                            item['auctionPeriod']['shouldStartAfter'])
    self.assertIn('T00:00:00+', item['auctionPeriod']['shouldStartAfter'])
    self.assertEqual(response.json['data']['next_check'], response.json['data']['enquiryPeriod']['endDate'])

    if self.initial_lots:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {
            'data': {"lots": [{"auctionPeriod": {"startDate": "9999-01-01T00:00:00+00:00"}}]}})
        item = response.json['data']["lots"][0]
    else:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id),
                                       {'data': {"auctionPeriod": {"startDate": "9999-01-01T00:00:00+00:00"}}})
        item = response.json['data']
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(item['auctionPeriod']['startDate'], '9999-01-01T00:00:00+00:00')

    if self.initial_lots:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id),
                                       {'data': {"lots": [{"auctionPeriod": {"startDate": None}}]}})
        item = response.json['data']["lots"][0]
    else:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id),
                                       {'data': {"auctionPeriod": {"startDate": None}}})
        item = response.json['data']
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('startDate', item['auctionPeriod'])


def reset_auction_period(self):
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
    self.assertGreaterEqual(response.json['data']['tenderPeriod']['endDate'],
                            item['auctionPeriod']['shouldStartAfter'])
    self.assertEqual(response.json['data']['next_check'], response.json['data']['enquiryPeriod']['endDate'])

    if self.initial_lots:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {
            'data': {"lots": [{"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}]}})
        item = response.json['data']["lots"][0]
    else:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id),
                                       {'data': {"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}})
        item = response.json['data']
    self.assertEqual(response.status, '200 OK')
    self.assertGreaterEqual(response.json['data']['tenderPeriod']['endDate'],
                            item['auctionPeriod']['shouldStartAfter'])
    self.assertIn('9999-01-01T00:00:00', item['auctionPeriod']['startDate'])

    self.set_status('active.auction', {'status': 'active.tendering'})
    response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']["status"], 'active.auction')
    item = response.json['data']["lots"][0] if self.initial_lots else response.json['data']
    self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'],
                            response.json['data']['enquiryPeriod']['endDate'])

    if self.initial_lots:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {
            'data': {"lots": [{"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}]}})
        item = response.json['data']["lots"][0]
    else:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id),
                                       {'data': {"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}})
        item = response.json['data']
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']["status"], 'active.auction')
    self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'],
                            response.json['data']['enquiryPeriod']['endDate'])
    self.assertIn('9999-01-01T00:00:00', item['auctionPeriod']['startDate'])
    self.assertIn('9999-01-01T00:00:00', response.json['data']['next_check'])

    now = get_now().isoformat()
    auction = self.db.get(self.auction_id)
    if self.initial_lots:
        auction['lots'][0]['auctionPeriod']['startDate'] = now
    else:
        auction['auctionPeriod']['startDate'] = now
    self.db.save(auction)

    response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']["status"], 'active.auction')
    item = response.json['data']["lots"][0] if self.initial_lots else response.json['data']
    self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'],
                            response.json['data']['enquiryPeriod']['endDate'])
    self.assertGreater(response.json['data']['next_check'], item['auctionPeriod']['startDate'])
    self.assertEqual(response.json['data']['next_check'], self.db.get(self.auction_id)['next_check'])

    if self.initial_lots:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {
            'data': {"lots": [{"auctionPeriod": {"startDate": response.json['data']['tenderPeriod']['endDate']}}]}})
        item = response.json['data']["lots"][0]
    else:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {
            'data': {"auctionPeriod": {"startDate": response.json['data']['enquiryPeriod']['endDate']}}})
        item = response.json['data']
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']["status"], 'active.auction')
    self.assertNotIn('9999-01-01T00:00:00', item['auctionPeriod']['startDate'])
    self.assertGreater(response.json['data']['next_check'], response.json['data']['enquiryPeriod']['endDate'])

    auction = self.db.get(self.auction_id)
    self.assertGreater(auction['next_check'], response.json['data']['enquiryPeriod']['endDate'])
    auction['enquiryPeriod']['endDate'] = auction['enquiryPeriod']['startDate']
    if self.initial_lots:
        auction['lots'][0]['auctionPeriod']['startDate'] = auction['enquiryPeriod']['startDate']
    else:
        auction['auctionPeriod']['startDate'] = auction['enquiryPeriod']['startDate']
    self.db.save(auction)

    response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
    if self.initial_lots:
        item = response.json['data']["lots"][0]
    else:
        item = response.json['data']
    self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'],
                            response.json['data']['enquiryPeriod']['endDate'])
    self.assertNotIn('next_check', response.json['data'])
    self.assertNotIn('next_check', self.db.get(self.auction_id))
    shouldStartAfter = item['auctionPeriod']['shouldStartAfter']

    response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {'data': {'id': self.auction_id}})
    if self.initial_lots:
        item = response.json['data']["lots"][0]
    else:
        item = response.json['data']
    self.assertEqual(item['auctionPeriod']['shouldStartAfter'], shouldStartAfter)
    self.assertNotIn('next_check', response.json['data'])

    if self.initial_lots:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id), {
            'data': {"lots": [{"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}]}})
        item = response.json['data']["lots"][0]
    else:
        response = self.app.patch_json('/auctions/{}'.format(self.auction_id),
                                       {'data': {"auctionPeriod": {"startDate": "9999-01-01T00:00:00"}}})
        item = response.json['data']
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.json['data']["status"], 'active.auction')
    self.assertGreaterEqual(item['auctionPeriod']['shouldStartAfter'],
                            response.json['data']['enquiryPeriod']['endDate'])
    self.assertIn('9999-01-01T00:00:00', item['auctionPeriod']['startDate'])
    self.assertIn('9999-01-01T00:00:00', response.json['data']['next_check'])


# InsiderAuctionAwardSwitchResourceTest
def switch_verification_to_unsuccessful(self):
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


def switch_payment_to_unsuccessful(self):
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


def switch_active_to_unsuccessful(self):
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


# InsiderAuctionAwardSwitch2ResourceTest
def switch_verification_to_unsuccessful2(self):
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


def switch_payment_to_unsuccessful2(self):
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


def switch_active_to_unsuccessful2(self):
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


# InsiderAuctionDontSwitchSuspendedAuction2ResourceTest
def switch_suspended_auction_to_auction(self):
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
    self.assertEqual(response.json['data']["status"], "active.auction")


# InsiderAuctionDontSwitchSuspendedAuctionResourceTest
def switch_suspended_verification_to_unsuccessful(self):
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


def switch_suspended_payment_to_unsuccessful(self):
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


def switch_suspended_active_to_unsuccessful(self):
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
