from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models


class SiteSettings(models.Model):
    """
    A singleton database model for storing application/API settings
    """

    # Prevent more than one setting object by associating it with the site
    site = models.ForeignKey(Site,
            blank=True,
            null=True)

    def save(self, *args, **kwargs):
        """
        Manually assign the site, and save the object
        """
        site = Site.objects.get(pk=settings.SITE_ID)
        self.site = site
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """
        Retrieve the settings object for the current site
        """
        settings_singleton,_ = cls.objects.get_or_create(
                site__pk=settings.SITE_ID)
        return settings_singleton


class UPSSettings(SiteSettings):
    """
    Account credentials and options for UPS API
    """
    user = models.CharField('Username',
            max_length=99,
            blank=True,
            null=True)
    password = models.CharField('Account Password',
            max_length=99,
            blank=True,
            null=True)
    license = models.CharField('License Number',
            max_length=50,
            blank=True,
            null=True)
    testing = models.BooleanField('Testing',
            default=True)


class SquareSettings(SiteSettings):
    """
    Account details and settings for the Square payment API
    """
    access_token = models.CharField('Access Token',
            max_length=100,
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

