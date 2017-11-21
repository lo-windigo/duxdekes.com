from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.sites.models import Site
from django.forms import formset_factory
#from django.views.generic.edit import UpdateView
from django.views.generic.base import View, TemplateResponseMixin
from django.http import HttpResponseRedirect
from duxdekes import models
import squareconnect
from squareconnect.apis.locations_api import LocationsApi
from squareconnect.rest import ApiException
from . import forms


class SettingsView(TemplateResponseMixin, View):
    """
    Edit the various API settings... dynamically!
    """
    template_name = 'dashboard/settings/settings_form.html'
    settings_forms = {
                'Primary': forms.SettingsForm,
                'Square': forms.SquareSettingsForm,
                'UPS': forms.UPSSettingsForm,
                }
    success_url = reverse_lazy('dashboard:index')


    def get(self, request, *args, **kwargs):
        """
        Serve up the forms with current settings
        """
        forms = self.get_forms()
        return self.render_to_response(self.get_context_data(forms=forms))


    def post(self, request, *args, **kwargs):
        """
        Process all forms, and send them to the right places
        """
        forms = self.get_forms()
        
        if all([form.is_valid() for form in forms.values()]):
            return self.forms_valid(forms)
        else:
            # TODO: Throw a wrench or something
            pass


    def get_context_data(self, *args, **kwargs):
        """
        Override get_context_data to fix the page title
        """
        context = {}
        context.update(**kwargs)
        context['title'] = 'Settings'
        choices = []

        square_settings = models.SquareSettings.get_settings()

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

        context['location_choices'] = choices

        return context


    def get_forms(self):
        """
        Instantiate all of the available forms
        """
        forms = {}

        for key, klass in self.settings_forms.items():
            
            if key == 'Primary':
                instance, _ = klass.Meta.model.objects.get_or_create(id=settings.SITE_ID)
            else:
                instance = klass.Meta.model.get_settings()

            kwargs = {
                    'instance': instance,
                    'prefix': key,
                    }

            if self.request.method in ('POST', 'PUT'):
                kwargs.update({'data': self.request.POST})
                
            forms[key] = klass(**kwargs)

        return forms


    def get_objects(self):
        """
        Get the only site in town
        """
        site, _ = Site.objects.get_or_create(pk=settings.SITE_ID)
        return site

