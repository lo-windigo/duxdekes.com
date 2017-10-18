from django import forms
from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_class
from oscar.forms import widgets

# Get the original form
AddToBasketForm = get_class('basket.forms', 'AddToBasketForm')


class UnfinishedAddToBasketForm(AddToBasketForm):
    """
    Overridden to remove undesired values from the product drop-down
    """
    def _create_parent_product_fields(self, product):
        """
        Removed attribute_summary description, otherwise function is the same
        """
        choices = []
        disabled_values = []
        for child in product.children.all():
            # Check if it is available to buy
            info = self.basket.strategy.fetch_for_product(child)
            if not info.availability.is_available_to_buy:
                disabled_values.append(child.id)

            choices.append((child.id, child.get_title()))

        self.fields['child_id'] = forms.ChoiceField(
            choices=tuple(choices), label=_("Material"),
            widget=widgets.AdvancedSelect(disabled_values=disabled_values))


class UnfinishedSimpleAddToBasketForm(UnfinishedAddToBasketForm):
    """
    Simplified version of the add to basket form where the quantity is
    defaulted to 1 and rendered in a hidden widget

    Copied VERBATIM from oscar, to allow the parent form changes to propagate
    """
    quantity = forms.IntegerField(
        initial=1, min_value=1, widget=forms.HiddenInput, label=_('Quantity'))

