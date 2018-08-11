import logging
from django.conf import settings
from duxdekes.models import SquareSettings
from oscar.apps.checkout.views import \
    PaymentDetailsView as OscarPaymentDetailsView, \
    ShippingAddressView as OscarShippingAddressView
from oscar.core.loading import get_model
from . import forms


Country = get_model('address', 'Country')
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
        submission = self.build_submission()
        if submission['payment_kwargs']['nonce']:
            return self.submit(**submission)
        
        logger.info('handle_place_order_submission() called without card nonce')
        msg = ("There was a problem with our payment processor. Please try "
            "again in a few minutes, and contact us if this problem persists.")

        return self.render_payment_details(request, error=msg)


    def handle_payment_details_submission(self, request):
        """
        Handle Square payment form submission
        """
        square_form = forms.SquareNonceForm(request.POST)

        if square_form.is_valid():
            self.save_card_nonce(square_form.cleaned_data['nonce'])
            return self.render_preview(request, square_form=square_form)
        
        logger.info('handle_payment_details_submission() called without card nonce')
        msg = ("There was a problem with our payment processor. Please try "
            "again in a few minutes, and contact us if this problem persists.")

        return self.render_payment_details(request, error=msg square_form=square_form)


class ShippingAddressView(OscarShippingAddressView):
    """
    Get a shipping address view
    """

    def get_initial(self):
        """
        Override the get_initial method to set US as the default choice for the
        Country field, as a sensible choice for most customers
        """
        initial = super().get_initial()

        if not initial:
            initial = dict()
            default_country = 'US'
            initial['country_id'] = default_country
            initial['country'] = Country.objects.get(iso_3166_1_a2=default_country)

        return initial

