from django.db import models
from oscar.apps.order.abstract_models import AbstractOrder


class Order(AbstractOrder):
    """
    Override the order model to add additional fields for post-order shipping
    """
    final_shipping = models.DecimalField("Final shipping charge",
            decimal_places=2, max_digits=12, default=0)


from oscar.apps.order.models import *  # noqa isort:skip
