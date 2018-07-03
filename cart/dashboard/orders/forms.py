from django import forms
from oscar.core.loading import get_class, get_model


class DiscountOrderForm(forms.Form):
    """
    A form used to accept a new basket total
    """
    final_basket_total = forms.DecimalField(label="Final basket total")

class FinalizeOrderForm(forms.Form):
    """
    A form specifically tailored to creating Instructions product
    """
    final_shipping = forms.DecimalField(label="Actual Shipping Cost")

