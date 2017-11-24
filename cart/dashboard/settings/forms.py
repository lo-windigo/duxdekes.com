from django import forms
from django.contrib.sites.models import Site
from duxdekes import models
import squareconnect
from squareconnect.apis.locations_api import LocationsApi
from squareconnect.rest import ApiException


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
        super().__init__(*args, **kwargs)

        access_token = getattr(self.instance, 'access_token', False)
        choices = []

        if not access_token:
            return

        squareconnect.configuration.access_token = access_token

        try:
            api_instance = LocationsApi()
            response = api_instance.list_locations()

            for location in response.locations:
                location_id = getattr(location, 'id', False)
                
                # Skip a location that doesn't provide a valid ID
                if not location_id:
                    pass

                try:
                    location_desc = location.name
                except:
                    location_desc = location_id

                choices.append((location_id, location_desc))

        except ApiException as e:
            choices.append((None, 'Problem accessing Square'))

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

