from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.sites.models import Site
from django.forms import formset_factory
from django.views.generic.edit import UpdateView
from duxdekes import models
import squareconnect
from squareconnect.apis.locations_api import LocationsApi
from squareconnect.rest import ApiException
from . import forms


class SettingsView(UpdateView):
    """
    Edit the various API settings... dynamically!
    """
    template_name = 'dashboard/settings/settings_form.html'
    form_class = forms.SettingsForm
    forms = {
            'square': forms.SquareSettingsForm,
            'ups': forms.UPSSettingsForm,
            }
    success_url = reverse_lazy('dashboard:index')

    def __init__(self, *args, **kwargs):
        """
        Set up the forms array
        """


    def get_context_data(self, *args, **kwargs):
        """
        Override get_context_data to fix the page title
        """
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Settings'
        return context


    def get_form_kwargs(self, *args, **kwargs):
        """
        Fetch locations from Square, and assign that to "choices"
        """
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        square_settings = models.SquareSettings.get_settings()
        choices = []

        if square_settings.access_token:
            squareconnect.configuration.access_token = \
                square_settings.access_token

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
            # TODO: Something smart, instead of this.
            #raise e
            pass

        form_kwargs.update({'location_choices': choices})

        return form_kwargs


    def get_object(self):
        """
        Get the only site in town
        """
        site, _ = Site.objects.get_or_create(pk=settings.SITE_ID)
        return site
