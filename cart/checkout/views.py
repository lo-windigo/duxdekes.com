from django.conf import settings
from oscar.core.loading import get_class
from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from . import forms


# Dynamically load some of Oscar's classes
OrderNumberGenerator = get_class('order.utils', 'OrderNumberGenerator')


class PaymentDetailsView(OscarPaymentDetailsView):

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

    def generate_order_number(self, basket):
        """
        Was not being carried over by Oscar's PaymentDetailsView
        """
        return OrderNumberGenerator().order_number(basket)

