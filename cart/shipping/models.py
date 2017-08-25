from django.db import models

class Box(models.Model):
    length = models.DecimalField(max_digits=5,
            decimal_places=2)
    width = models.DecimalField(max_digits=5,
            decimal_places=2)
    height = models.DecimalField(max_digits=5,
            decimal_places=2)

    def __str__(self):
        """
        Define a better string representation for the admin
        """
        return '{}" x {}" x {}"'.format(self.length, self.width, self.height)

from oscar.apps.shipping.models import *  # noqa

