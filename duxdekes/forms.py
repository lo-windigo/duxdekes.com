
from django import forms


class ContactForm(forms.Form):
    """
    The form used to send messages through the Contact page
    """
    name = forms.CharField(max_length=100,
            widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    url = forms.CharField(required=False, label='Please ignore this field')
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


    def is_valid(self):
        """
        Check to make sure our false URL field is empty
        """
        if len(self.data['url']) > 0:
            return False

        return super().is_valid()    

