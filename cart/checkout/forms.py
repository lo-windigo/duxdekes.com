from django import forms


class SquareNonceForm(forms.Form):
    """
    A form used to submit the Squareconnect nonce value
    """
    nonce = forms.CharField(max_length=300, widget=forms.HiddenInput)

