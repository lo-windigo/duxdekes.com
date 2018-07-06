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
    def basket_charge_override(self):
        """
        Returns boolean indicating whether or not the basket total value has
        been overridden
        """
        return self.final_basket_total and self.final_basket_total > 0

    @property
    def shipping_charge_finalized(self):
        """
        Returns boolean indicating whether or not the shipping charge has
        been finalized
        """
        return self.final_shipping and self.final_shipping > 0

    @property
    def final_basket_charge(self):
        """
        Return the final basket total, whether it is an adjusted value or the
        default oscar value
        """
        if self.basket_charge_override:
            return self.final_basket_total

        return self.basket_total_incl_tax

    @property
    def final_shipping_charge(self):

        # If we have an override set on this order, return that value
        if self.shipping_charge_finalized:
            return self.final_shipping

        # Default to the normal shipping total
        return self.shipping_incl_tax


from oscar.apps.order.models import *  # noqa isort:skip
