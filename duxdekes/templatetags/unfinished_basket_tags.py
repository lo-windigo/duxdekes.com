from django import template

from oscar.core.compat import assignment_tag
from oscar.core.loading import get_class, get_model

AddToBasketForm = get_class('basket.forms', 'UnfinishedAddToBasketForm')
SimpleAddToBasketForm = get_class('basket.forms', 'UnfinishedSimpleAddToBasketForm')
Product = get_model('catalogue', 'product')

register = template.Library()

QNT_SINGLE, QNT_MULTIPLE = 'single', 'multiple'


@assignment_tag(register)
def unfinished_basket_form(request, product, quantity_type='single'):
    """
    Verbatim copied from Oscar code - just overriding forms, and changing the
    name to avoid collisions
    """
    if not isinstance(product, Product):
        return ''

    initial = {}
    if not product.is_parent:
        initial['product_id'] = product.id

    form_class = AddToBasketForm
    if quantity_type == QNT_SINGLE:
        form_class = SimpleAddToBasketForm

    form = form_class(request.basket, product=product, initial=initial)

    return form
