
from django import forms


class ContactForm(forms.Form):
    """
    The form used to send messages through the Contact page
    """
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

