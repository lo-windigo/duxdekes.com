from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models


class SquareSettings(models.Model):
    """
    Save any settings required for the Square API
    """

    # Prevent more than one setting object
    site = models.OneToOneField(Site,
            blank=True,
            null=True)
    access_token = models.CharField('Access Token',
            max_length=50,
            blank=True,
            null=True)
    application_id = models.CharField('Application ID',
            max_length=50,
            blank=True,
            null=True)
    location_desc = models.CharField('Location Description',
            max_length=250,
            blank=True,
            null=True)
    location_id = models.CharField('Location ID',
            max_length=50,
            blank=True,
            null=True)


    def __init__(self, *args, **kwargs):
        """
        Manually assign the site, and save the object
        """
        if not settings.SITE_ID:
            raise Exception('SITE_ID not set in settings.py')

        self.site = settings.SITE_ID
        super().__init__(*args, **kwargs)


from oscar.apps.checkout.models import *  # noqa

