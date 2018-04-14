from oscar.apps.checkout import session
from . import tax


#http://django-oscar.readthedocs.io/en/releases-1.1/howto/how_to_handle_us_taxes.html?highlight=DeferredTax
class CheckoutSessionMixin(session.CheckoutSessionMixin):

    def build_submission(self, **kwargs):
        submission = super(CheckoutSessionMixin, self).build_submission(
            **kwargs)

        if submission['shipping_address'] and submission['shipping_method']:
            tax.apply_to(submission)

            # Recalculate order total to ensure we have a tax-inclusive total
            submission['order_total'] = self.get_order_totals(
                submission['basket'],
                shipping_charge=submission['shipping_charge'])

        # Add extra information for Square chargeback protection
        # ( billing_address is already sent into the payment kwargs )
        if submission['user'] and submission['user'].email:
            email = submission['user'].email
        elif submission['guest_email']:
            email = submission['guest_email']
        if email:
            submission['payment_kwargs']['email'] = email
        submission['payment_kwargs']['shipping_address'] = shipping_address

        return submission

