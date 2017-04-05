
from oscar.apps.catalogue.app import BaseCatalogueApplication


class CatalogueApplication(BaseCatalogueApplication):
    """
    Composite class combining Products with Reviews
    """


application = CatalogueApplication()
