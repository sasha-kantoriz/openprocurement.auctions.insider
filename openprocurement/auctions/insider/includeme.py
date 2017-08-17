from openprocurement.auctions.insider.models import DGFInsider


def includeme(config):
    config.add_auction_procurementMethodType(DGFInsider)
    config.scan("openprocurement.auctions.insider.views")
