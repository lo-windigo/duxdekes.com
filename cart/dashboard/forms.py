from django import forms
from duxdekes.util import products
from oscar.core.loading import get_classes, get_model

Product = get_model('catalogue', 'Product')


class ProductForm(forms.Form):
    """
    A generic product form, containing common fields
    """
    title = forms.CharField(label="Title", max_length=200)


class UnfinishedForm(ProductForm):
    """
    A form specifically tailored to creating an Unfinished Blank product
    """
    pine_sku = forms.CharField(label="Pine ID",
            max_length=64,
            required=False)
    pine_price = forms.DecimalField(label="Pine Price",
            min_value=0,
            decimal_places=2,
            max_digits=12,
            required=False)
    tupelo_sku = forms.CharField(label="Tupelo ID",
            max_length=64,
            required=False)
    tupelo_price = forms.DecimalField(label="Tupelo Price",
            min_value=0,
            decimal_places=2,
            max_digits=12,
            required=False)
    feet_price = forms.DecimalField(label="Optional Feet Price",
            min_value=0,
            decimal_places=2,
            max_digits=12,
            required=False)


    def save_product(self):
        """
        Create/update a product object based on form data
        """
        if not self.is_valid():
            raise Exception('save_product() called on invalid form')

        products.add_unfinished(**self.cleaned_data)



class FinishedForm(ProductForm):
    """
    A form specifically tailored to creating a Finished Carving product
    """
    decoy_id = forms.CharField(label="Pine ID",
            max_length=64)
    price = forms.CharField(label="Pine Price",
            max_length=200)


class InstructionsForm(ProductForm):
    """
    A form specifically tailored to creating Instructions product
    """
    pass
