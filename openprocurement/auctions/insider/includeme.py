from pyramid.interfaces import IRequest

from openprocurement.auctions.core.includeme import IContentConfigurator

from openprocurement.auctions.insider.models import DGFInsider, IInsiderAuction
from openprocurement.auctions.insider.adapters import AuctionInsiderConfigurator
from openprocurement.auctions.insider.constants import (
    VIEW_LOCATIONS, PROCUREMENT_METHOD_TYPES
)


def includeme(config):
    for procurementMethodType in PROCUREMENT_METHOD_TYPES:
        config.add_auction_procurementMethodType(DGFInsider,
                                                 procurementMethodType)

    for view_module in VIEW_LOCATIONS:
        config.scan(view_module)

    config.registry.registerAdapter(
        AuctionInsiderConfigurator,
        (IInsiderAuction, IRequest),
        IContentConfigurator
    )
