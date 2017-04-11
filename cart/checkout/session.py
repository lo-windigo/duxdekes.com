from oscar.apps.checkout import session
from . import tax


#http://django-oscar.readthedocs.io/en/releases-1.1/howto/how_to_handle_us_taxes.html?highlight=DeferredTax
class CheckoutSessionMixin(session.CheckoutSessionMixin):

    def build_submission(self, **kwargs):
        submission = super(CheckoutSessionMixin, self).build_submission(
            **kwargs)

        if submission['shipping_address']:
            tax.apply_to(submission)

            # Recalculate order total to ensure we have a tax-inclusive total
            submission['order_total'] = self.get_order_totals(
                submission['basket'],
                shipping_method=submission['shipping_method'])

        return submission

