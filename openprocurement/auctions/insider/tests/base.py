# -*- coding: utf-8 -*-
import os
from datetime import datetime
from copy import deepcopy

from openprocurement.auctions.dgf.tests.base import (
    BaseWebTest,
    BaseFinancialAuctionWebTest,
    test_financial_organization,
    test_financial_auction_data,
    test_financial_auction_data_with_schema,
    test_financial_bids,
    schema_properties,
    test_lots,
)


now = datetime.now()
test_organization = deepcopy(test_financial_organization)
test_procuringEntity = test_organization.copy()

test_insider_auction_data = deepcopy(test_financial_auction_data)
test_insider_auction_data_with_schema = deepcopy(test_financial_auction_data_with_schema)

for data in test_insider_auction_data, test_insider_auction_data_with_schema:
    data["procurementMethodType"] = "dgfInsider"
    del data['minimalStep']

class BaseInsiderWebTest(BaseWebTest):

    """Base Web Test to test openprocurement.auctions.insider.

    It setups the database before each test and delete it after.
    """

    relative_to = os.path.dirname(__file__)


class BaseInsiderAuctionWebTest(BaseFinancialAuctionWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = test_insider_auction_data
    initial_organization = test_organization
