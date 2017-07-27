from decimal import Decimal as D
from django.conf import settings
from oscar.apps.shipping import methods
from oscar.core import prices
from oscar.core.loading import get_class, get_model
from ups_json.rating import UPSRating


InvalidShippingEvent = get_class('order.exceptions', 'InvalidShippingEvent')
WeightBased = get_model('shipping', 'WeightBased')


class DomesticShipping(methods.Base):
    code = 'UPS'
    name = 'UPS Ground'
    description = '''
    Shipping via UPS Ground services, delivered within 1-5 business days of
    packaging and shipping.
    '''
    address = None

    def __init__(self, shipping_address=None):
        """
        Initialize this shipping method with a shipping address for rate
        calculation
        """
        if not shipping_address:
            raise InvalidShippingEvent(
                '{} cannot be used without a shipping address'.format(
                    self.name))

        self.address = shipping_address


    def calculate(self, basket):

        rateRequest = UPSRating(settings.UPS_ACCOUNT,
                settings.UPS_PASSWORD,
                settings.UPS_LICENSE_NUMBER,
                settings.UPS_TESTING)

        weight = Scale.weigh_basket(basket)

        rate = rateRequest.get_rate(box, box, box, weight, self.address, UPS_SHIPPER)

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
            excl_tax=D('10.00'),
            incl_tax=D('10.00'))

