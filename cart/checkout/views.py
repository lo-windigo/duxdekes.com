import logging
from django.conf import settings
from duxdekes.models import SquareSettings
from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from . import forms


logger = logging.getLogger('cart.checkout.views')


class PaymentDetailsView(OscarPaymentDetailsView):
    """
    Enable our site to accept payments
    """

    def get_context_data(self, **kwargs):
        """
        Provide the square nonce form in context
        """
        ctx = super().get_context_data(**kwargs)
        square_settings = SquareSettings.get_settings()

        ctx['square_form'] = kwargs.get('square_form', forms.SquareNonceForm())
        ctx['square_app'] = square_settings.application_id

        return ctx


    def handle_place_order_submission(self, request):
        """
        Handle Square payment form submission
        """
        if self.get_card_nonce():
            return self.submit(**self.build_submission())
        
        logger.info('handle_place_order_submission() called without card nonce')

        # TODO: set error, prompt user?
        return self.render_preview(request)


    def handle_payment_details_submission(self, request):
        """
        Handle Square payment form submission
        """
        square_form = forms.SquareNonceForm(request.POST)

        if square_form.is_valid():
            self.save_card_nonce(square_form.cleaned_data['nonce'])
            return self.render_preview(request)
        
        logger.info('handle_payment_details_submission() called without card nonce')
        # TODO: Create/set an error message?
        return self.render_payment_details(request, square_form=square_form)

