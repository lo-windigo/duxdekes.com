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
    location_id = models.CharField('Location ID',
            max_length=50,
            blank=True,
            null=True)


    def save(self, *args, **kwargs):
        """
        Manually assign the site, and save the object
        """
        if not settings.SITE_ID:
            raise Exception('SITE_ID not set in settings.py')

        site = Site.objects.get(pk=settings.SITE_ID)
        self.site = site
        super().save(*args, **kwargs)


    def get_settings(self):
        square_settings,_ = self.objects.get_or_create(
                site__pk=settings.SITE_ID)
        return square_settings


from oscar.apps.checkout.models import *  # noqa

