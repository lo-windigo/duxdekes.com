from oscar.core.loading import get_class
from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from . import forms


class PaymentDetailsView(OscarPaymentDetailsView):

    def handle_payment_details_submission(self, request):
        """
        Handle Square payment form submission
        """
        square_form = forms.SquareNonceForm(request.POST)

        if square_form.is_valid():
            return self.render_preview(request, form=square_form)
        
        return self.render_payment_details(request, form=square_form)

