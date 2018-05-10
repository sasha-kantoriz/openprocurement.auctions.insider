# -*- coding: utf-8 -*-
from openprocurement.auctions.insider.models import DGFInsider
from openprocurement.auctions.core.adapters import (
    AuctionConfigurator,
    AuctionManagerAdapter
)
from openprocurement.auctions.core.plugins.awarding.v3.adapters import (
    AwardingV3ConfiguratorMixin
)


class AuctionInsiderConfigurator(AuctionConfigurator,
                                 AwardingV3ConfiguratorMixin):
    name = 'Auction Insider Configurator'
    model = DGFInsider


class AuctionInsiderManagerAdapter(AuctionManagerAdapter):

    def create_auction(self, request):
        pass

    def change_auction(self, request):
        pass
