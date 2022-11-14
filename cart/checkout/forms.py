from django import forms
from oscar.apps.checkout.forms import \
        ShippingAddressForm as OscarShippingAddressForm


class ShippingAddressForm(OscarShippingAddressForm):
    """
    Override the shipping address form to make the phone number field required
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].required = True

    class Meta(OscarShippingAddressForm.Meta):
        fields = [
            'title', 'first_name', 'last_name',
            'line1', 'line2', 'line3', 'line4',
            'postcode', 'country', 'state',
            'phone_number', 'notes',
        ]


class SquareTokenForm(forms.Form):
    """
    A form used to submit the Square token value
    """
    token = forms.CharField(max_length=300, widget=forms.HiddenInput)

