from oscar.apps.shipping import repository
from . import methods


class Repository(repository.Repository):

    def get_available_shipping_methods(
            self, basket, user=None, shipping_addr=None,
            request=None, **kwargs):
        
        if shipping_addr and shipping_addr.country.code == 'US':
            return (methods.DomesticShipping(),)
        else:
            return (methods.InternationalShipping(),)
