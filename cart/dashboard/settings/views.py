from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.sites.models import Site
from django.forms import formset_factory
#from django.views.generic.edit import UpdateView
from django.views.generic.base import View, TemplateResponseMixin
from django.http import HttpResponseRedirect
from duxdekes import models
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


    def forms_invalid(self, forms):
        """
        Called if the form data didn't check out
        """
        return self.render_to_response(self.get_context_data(forms=forms))


    def forms_valid(self, forms):
        """
        All the forms are valid; please save the data
        """
        for _,form in forms.items():
            form.save()

        return HttpResponseRedirect(self.success_url)


    def get(self, request, *args, **kwargs):
        """
        Serve up the forms with current settings
        """
        forms = self.get_forms()
        return self.render_to_response(self.get_context_data(forms=forms))


    def get_context_data(self, *args, **kwargs):
        """
        Override get_context_data to fix the page title
        """
        context = {}
        context.update(**kwargs)
        context['title'] = 'Settings'

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


    def post(self, request, *args, **kwargs):
        """
        Process all forms, and send them to the right places
        """
        forms = self.get_forms()
        
        if all([form.is_valid() for form in forms.values()]):
            return self.forms_valid(forms)

        return self.forms_invalid(forms)

