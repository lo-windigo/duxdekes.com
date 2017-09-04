from decimal import Decimal as D
from django.conf import settings
from oscar.apps.checkout.utils import CheckoutSessionData
from oscar.apps.shipping import methods, scales 
from oscar.core import prices
from oscar.core.loading import get_class, get_model
from ups_json.base import UPSAddress
from ups_json.rating import UPSRating


InvalidShippingEvent = get_class('order.exceptions', 'InvalidShippingEvent')
Box = get_model('shipping', 'Box')
WeightBased = get_model('shipping', 'WeightBased')


class DomesticShipping(methods.Base):
    code = 'UPS'
    name = 'UPS Ground'
    description = '''
    Shipping via UPS Ground services, delivered within 1-5 business days of
    packaging and shipping. Rate is calculated AFTER address has been entered.
    '''
    def __init__(self):
        """
        Quickly init the default box as a dictionary
        """
        box = Box()

        box.length = 0
        box.width = 0
        box.height = 0

        self.box = box


    def calculate(self, basket):
        """
        Get a rate for this package from UPS
        """

        # TODO: Implement actual address check
        if True:
            return prices.Price(
                currency=basket.currency,
                excl_tax=D(0))


        # Temporary address - DAMNIT
        address = UPSAddress()
        address.name = "SHIP 2 ME"
        rate_request = UPSRating(settings.UPS_ACCOUNT,
                settings.UPS_PASSWORD,
                settings.UPS_LICENSE_NUMBER,
                settings.UPS_TESTING)
        scale = scales.Scale()
        weight = scale.weigh_basket(basket)
 
        #for item in basket.get_lines():
        #    box = 

        # TEMPORARY BOX CRAP
        box = self.box

        rate = rate_request.get_rate(box.length, box.width, box.height, weight,
                address, settings.UPS_SHIPPER)

        return prices.Price(
            currency=basket.currency,
            excl_tax=rate)


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

