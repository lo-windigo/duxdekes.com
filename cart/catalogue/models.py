from oscar.apps.catalogue.models import *  # noqa
from django.contrib.flatpages import FlatPage
from django.db import models



class InstructionProduct(Product):
    """
    Override the usual product model to allow attaching an unfinished
    blank to bundle
    """
    blank = models.ForeignKey(Product,
            blank = True,
            null = True)


class InstructionProduct(Product):
    extra_content = models.ForeignKey(FlatPage,
            blank = True,
            null = True)

