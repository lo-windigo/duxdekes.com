from oscar.apps.shipping import repository
from . import methods


class Repository(repository.Repository):

    def get_available_shipping_methods(
            self, basket, user=None, shipping_addr=None,
            request=None, **kwargs):
        
        # For now, only return UPS
        return (methods.DomesticShipping(),)

        if shipping_addr:
            if shipping_addr.country.code == 'US':
                return (methods.DomesticShipping(),)
            else:
                return (methods.InternationalShipping(),)
        else:
            # We need a return value before details have been entered, for
            # presenting the basket originally
            return (methods.DomesticShipping(), methods.InternationalShipping())
