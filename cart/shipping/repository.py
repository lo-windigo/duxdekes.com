from oscar.apps.shipping import repository
from oscar.core.loading import get_class
from . import methods


class Repository(repository.Repository):

    def get_available_shipping_methods(
            self, basket, user=None, shipping_addr=None,
            request=None, **kwargs):
        
        if shipping_addr:
            #if shipping_addr.country.code == 'US':
            #    return (methods.DomesticShipping(shipping_addr),)
            #else:
            #    return (methods.InternationalShipping(shipping_addr),)
            return (methods.DomesticShipping(shipping_addr),)
        else:
            # We need a return value before details have been entered, for
            # presenting the basket originally
            return (methods.DomesticShipping())

