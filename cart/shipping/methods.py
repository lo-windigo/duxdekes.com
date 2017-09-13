from decimal import Decimal as D
from django.conf import settings
from oscar.apps.checkout.utils import CheckoutSessionData
from oscar.apps.shipping import methods, scales 
from oscar.core import prices
from oscar.core.loading import get_class, get_model
from ups_json.rating import UPSRating


InvalidShippingEvent = get_class('order.exceptions', 'InvalidShippingEvent')
Box = get_model('shipping', 'Box')


class DomesticShipping(methods.Base):
    """
    Provide a method of standard UPS ground shipping
    """
    code = 'UPS'
    name = 'UPS Ground'
    description = '''
    Shipping via UPS Ground services, delivered within 1-5 business days of
    packaging and shipping. Rate is calculated AFTER address has been entered.
    '''
    shipping_addr = None


    def __init__(self, shipping_addr=None):
        """
        Quickly init the default box, and save the shipping address
        """
        self.shipping_addr = shipping_addr
        if not shipping_addr:
            self.name = '{} (rated after address entered)'.format(self.name)


    def calculate(self, basket):
        """
        Get a rate for this package from UPS
        """
        if not self.shipping_addr:
            return prices.Price(
                currency=basket.currency,
                excl_tax=D(0))

        # Temporary address - DAMNIT
        address = {}

        # Initialize a rate request object
        rate_request = UPSRating(settings.UPS_ACCOUNT,
                settings.UPS_PASSWORD,
                settings.UPS_LICENSE_NUMBER,
                settings.UPS_TESTING)
        # TODO: Allow rating entire basket
        #scale = scales.Scale()
        #weight = scale.weigh_basket(basket)
 
        # Compile the address dictionary
        address['name'] = '{} {}'.format(self.shipping_addr.get('first_name', ''),
            self.shipping_addr.get('last_name', ''))
        address['postal_code'] = self.shipping_addr.postcode
        address['city'] = self.shipping_addr.line4
        address['state_province'] = self.shipping_addr.state

        # Append any address lines to the list
        address['lines'] = []
        for i in range(1, 3):
            try:
                address['lines'].append(self.shipping_address.get('line{}'.format(i)))
            except:
                pass

        # TODO: Consolidate items into one box, if applicable?
        for item in basket.get_lines():
            boxes.append(item.attr.box) 

        rate = rate_request.get_rate(box.length, box.width, box.height, weight,
                address, settings.UPS_SHIPPER)

        if self.shipping_address.state.upper() == 'NY':
            rate_incl_tax = rate * D(1.07)
        else:
            rate_incl_tax = rate

        return prices.Price(
            currency=basket.currency,
            excl_tax=rate,
            incl_tax=rate_incl_tax)


class InternationalShipping(methods.Base):
    code = 'USPS'
    name = 'International'
    description = 'US Postal Service priority shipping'

    def calculate(self, basket):

	# TODO: International? Gaaaaaaaah
        # TODO: Also include tax for incl_tax value
        return prices.Price(
            currency=basket.currency,
            excl_tax=D('10.00'))

