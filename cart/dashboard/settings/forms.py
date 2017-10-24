from django import forms
from django.contrib.sites.models import Site
from duxdekes import models


class SettingsForm(forms.ModelForm):
    """
    Generic umbrella form for site settings
    """
    class Meta:
        model = Site
        fields = ['name', 'domain']


class SquareSettingsForm(forms.ModelForm):
    """
    Allow editing the API keys and location ID for the Square API
    """
    def __init__(self, *args, **kwargs):
        """
        Set the location choices dynamically
        """
        choices = []

        if 'location_choices' in kwargs:
            choices = kwargs.pop('location_choices', None)

        super().__init__(*args, **kwargs)

        self.fields['location_id'].widget = forms.Select(choices=choices)


    class Meta:
        model = models.SquareSettings
        exclude = ['location_desc', 'site']
        widgets = {
                'location_id': forms.Select,
                }


class UPSSettingsForm(forms.ModelForm):
    """
    Allow editing the UPS Account & license numbers
    """
    class Meta:
        model = models.UPSSettings
        exclude = ['site']
        widgets = {
                'password': forms.PasswordInput,
                }

