from django import forms
from oscar.core.loading import get_class, get_model


class FinalizeOrderForm(forms.Form):
    """
    A form specifically tailored to creating Instructions product
    """
    final_shipping = forms.DecimalField(label="Actual Shipping Cost")

