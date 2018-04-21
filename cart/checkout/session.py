from oscar.apps.checkout import session
from . import tax


#http://django-oscar.readthedocs.io/en/releases-1.1/howto/how_to_handle_us_taxes.html?highlight=DeferredTax
class CheckoutSessionMixin(session.CheckoutSessionMixin):

    def build_submission(self, **kwargs):
        submission = super().build_submission(**kwargs)

        # If a shipping address is present, save it for the payment kwargs
        if hasattr(submission, 'shipping_address') and hasattr(submission,
                'shipping_method'):

            # Copy the shipping address object to the payment kwargs to provide
            # to Square (provides chargeback protection)
            submission['payment_kwargs']['shipping_address'] = submission['shipping_address']

            tax.apply_to(submission)

            # Recalculate order total to ensure we have a tax-inclusive total
            submission['order_total'] = self.get_order_totals(
                submission['basket'],
                shipping_charge=submission['shipping_charge'])

        # Add user email to payment kwargs formation for Square chargeback protection
        # ( billing_address is already sent into the payment kwargs )
        if hasattr(submission, 'user') and hasattr(submission['user'], email):
            email = submission['user'].email
        elif hasattr(submission, 'guest_email'):
            email = submission['guest_email']
        else:
            email = False

        if email:
            submission['payment_kwargs']['email'] = email

        return submission

