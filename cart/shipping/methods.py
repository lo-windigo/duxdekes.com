from oscar.apps.shipping import methods
from oscar.core import prices
from decimal import Decimal as D


class DomesticShipping(methods.Base):
    code = 'UPS'
    name = 'UPS'
    description = 'UPS priority shipping'

    def calculate(self, basket):

	# TODO: query UPS? For now, just append $5.00 on it all
        # TODO: Also include tax for incl_tax value
        return prices.Price(
            currency=basket.currency,
            excl_tax=D('5.00'),
            incl_tax=D('5.00'))


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

