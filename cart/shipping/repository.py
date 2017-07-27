from oscar.apps.shipping import repository
from . import methods


class Repository(repository.Repository):

    def get_available_shipping_methods(
            self, basket, user=None, shipping_addr=None,
            request=None, **kwargs):
        
        if shipping_addr:
            if shipping_addr.country.code == 'US':
                return (methods.DomesticShipping(shipping_addr),)
            else:
                return (methods.InternationalShipping(shipping_addr),)
        else:
            raise Exception('No shipping address provided!')
