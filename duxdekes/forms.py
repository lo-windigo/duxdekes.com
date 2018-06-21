
from django import forms


class ContactForm(forms.Form):
    """
    The form used to send messages through the Contact page
    """
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    url = forms.CharField(required=True, label='Please ignore this field')
    message = forms.CharField(widget=forms.Textarea)


    def is_valid(self):
        """
        Check to make sure our false URL field is empty
        """

        if len(self.data['url']) > 0:
            return false

        return super().is_valid()    

