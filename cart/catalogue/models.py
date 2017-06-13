from oscar.apps.catalogue.models import *  # noqa
from oscar.core.loading import get_model
from django.db import models





class InstructionsProduct(Product):
    """
    Override the usual product model to allow attaching an unfinished
    blank to bundle
    """
    blank = models.ForeignKey(Product,
            related_name='matching_blank',
            required=False,
            blank=True,
            null=True)


#class BookInstructionsProduct(Product):
#    """
#    Override the usual product model to include extra descriptive content
#    """
#    extra_content = models.ForeignKey(FlatPage,
#            blank = True,
#            null = True)

