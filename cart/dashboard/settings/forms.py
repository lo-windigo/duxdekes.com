from django import forms
from cart.checkout import models


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

