from django.conf import settings
from oscar.core.loading import get_class
from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from . import forms


class PaymentDetailsView(OscarPaymentDetailsView):
    """
    Enable our site to accept payments
    """

    def get_context_data(self, **kwargs):
        """
        Provide the square nonce form in context
        """
        ctx = super().get_context_data(**kwargs)

        ctx['form'] = forms.SquareNonceForm()
        ctx['square_app'] = settings.SQUARE_APPLICATION_ID

        return ctx


    def handle_payment_details_submission(self, request):
        """
        Handle Square payment form submission
        """
        square_form = forms.SquareNonceForm(request.POST)

        if square_form.is_valid():
            return self.render_preview(request, form=square_form)
        
        return self.render_payment_details(request, form=square_form)

