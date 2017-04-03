from oscar.apps.shipping import methods
from oscar.core import prices
from decimal import Decimal as D


class UPS(methods.Base):
    code = 'UPS'
    name = 'UPS'
    description = 'UPS priority shipping'

    def calculate(self, basket):

	# TODO: query UPS? For now, just append $5.00 on it all
        return prices.Price(
            currency=basket.currency,
            excl_tax=D('5.00'), incl_tax=D('5.00'))

