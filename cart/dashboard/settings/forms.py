from django import forms
from django.contrib.sites.models import Site
from duxdekes import models
from duxdekes.util import square


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

        client = square.get_client()
        
        if not client:
            return

        try:
            response = client.locations.list_locations()

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

        except Exception as e:
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
                # Display the password in a password field, and include the
                # previous value if present
                'password': forms.PasswordInput(render_value=True),
                }

