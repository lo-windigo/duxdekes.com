from django.db import models
from oscar.apps.order.abstract_models import AbstractOrder


class Order(AbstractOrder):
    """
    Override the order model to add additional fields for post-order shipping
    """
    final_shipping = models.DecimalField("Final shipping charge",
            decimal_places=2, max_digits=12, default=0)
    final_basket_total = models.DecimalField("Final basket total",
            decimal_places=2, max_digits=12, default=0)

    @property
    def final_basket_charge(self):

        # If we have an override set on this order, return that value
        if self.basket_charge_override:
            return self.final_basket_total

        # Default to the normal basket total
        return self.basket_total_incl_tax

    @property
    def basket_charge_override(self):
        return self.final_basket_total and self.final_basket_total > 0


from oscar.apps.order.models import *  # noqa isort:skip
