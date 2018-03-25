import logging, sys
from decimal import Decimal as D
from django.conf import settings
from duxdekes import models
from duxdekes.util import tax
from oscar.apps.checkout.utils import CheckoutSessionData
from oscar.apps.shipping import methods, scales 
from oscar.core import prices
from oscar.core.loading import get_class, get_model
from ups_json.rating import UPSRating


InvalidShippingEvent = get_class('order.exceptions', 'InvalidShippingEvent')
Box = get_model('shipping', 'Box')
Product = get_model('catalogue', 'Product')
logger = logging.getLogger(__name__)


class DomesticShipping(methods.Base):
    """
    Provide a method of standard UPS ground shipping
    """
    code = 'UPS'
    name = 'UPS Ground'
    description = '''
    Shipping via UPS Ground services, delivered within 1-5 business days of
    packaging and shipping.
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
        if not self.shipping_addr or not basket.all_lines():
            return prices.Price(
                currency=basket.currency,
                excl_tax=D(0),
                incl_tax=D(0))

        # Initialize a rate request object
        ups_settings = models.UPSSettings.get_settings()
        rate_request = UPSRating(ups_settings.user,
                ups_settings.password,
                ups_settings.license,
                ups_settings.testing)
 
        # Compile the address dictionary
        address = {
                'name': '{} {}'.format(getattr(self.shipping_addr,
                    'first_name', ''),
                    getattr(self.shipping_addr, 'last_name', '')),
                'postal_code': self.shipping_addr.postcode,
                'city': self.shipping_addr.line4,
                'state_province': self.shipping_addr.state,
                'country_code': self.shipping_addr.country.code,
                'lines': [],
                }

        # Append any address lines to the list
        for i in range(1, 4):
            try:
                address['lines'].append(getattr(self.shipping_addr,
                    'line{}'.format(i)))
            except:
                pass

        # Start with $1, to pay for shipping container
        rate = D(1)
        
        for item in basket.all_lines():

            # Make sure we are pulling the correct attributes for child products
            if item.product.structure == Product.CHILD:
                product = item.product.parent
            else:
                product = item.product

            try:
                box = product.attr.box 
                item_rate = rate_request.get_rate(box.length, box.width, box.height,
                        product.attr.weight, address, settings.UPS_SHIPPER)

                rate = rate + (item_rate * item.quantity)
            except:
                # Log the error
                logger.warn('Could not rate item %s for shipping', product.upc)
                

        if self.shipping_addr and self.shipping_addr.state.upper() == 'NY':
            rate_incl_tax = rate + tax.calculate_sales_tax(rate) 
        else:
            rate_incl_tax = rate

        return prices.Price(
            currency=basket.currency,
            excl_tax=rate,
            incl_tax=rate_incl_tax)


#class InternationalShipping(methods.Base):
#    code = 'USPS'
#    name = 'International'
#    description = 'US Postal Service priority shipping'
#
#    def calculate(self, basket):
#
#	# TODO: International? Gaaaaaaaah
#        # TODO: Also include tax for incl_tax value
#        return prices.Price(
#            currency=basket.currency,
#            excl_tax=D('10.00'))

