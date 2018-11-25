import logging, sys
from decimal import Decimal as D
from django.conf import settings
from duxdekes import models
from duxdekes.util import tax
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
        ups = UPSRating(ups_settings.user,
                ups_settings.password,
                ups_settings.license,
                ups_settings.testing)
 
        # Start with $1, to pay for shipping container
        rate = D(1)
        
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

        # Rate the items in the basket
        for item in basket.all_lines():
           rate += rate_item(item, ups, address) * item.quantity

        # Handle taxes
        rate_incl_tax = rate
        if self.shipping_addr and self.shipping_addr.state.upper() == 'NY':
            rate_incl_tax += tax.calculate_sales_tax(rate) 

        return prices.Price(
            currency=basket.currency,
            excl_tax=rate,
            incl_tax=rate_incl_tax)


def rate_item(product, ups, address):
    """
    Rate a single item for shipping
    """

    # Make sure we are pulling the correct attributes for child products
    if product.structure == Product.CHILD:
        product = product.parent

    # Before rating, make sure this item doesn't have free shipping
    try:
        if product.attr.free_shipping:
            return D(0)
    except:
        pass

    # Try to get the package rate from UPS
    try:
        box = product.attr.box 
        item_rate = ups.get_rate(box.length, box.width, box.height,
                product.attr.weight, address, settings.UPS_SHIPPER)

    except Exception as e:
        err = 'Could not rate "%s" for shipping; adding $20. Error: %s'
        logger.warn(err, product.upc, e)

        # If the rate cannot be gathered, add in a very high estimate
        item_rate = D(20)

    return item_rate

