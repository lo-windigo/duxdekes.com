from django import forms
from duxdekes.util import products
from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')


class ProductForm(forms.ModelForm):
    """
    A generic product form, containing common fields
    """
    class Meta:
        model = Product
        fields = ['title', 'upc']


class FinishedForm(ProductForm):
    """
    A form specifically tailored to creating a finished decoy
    """
    price = forms.DecimalField(label="Price",
            min_value=0,
            decimal_places=2,
            max_digits=12,
            required=False)


    # Make the product_class field NOT REQUIRED, FOR THE LOVE OF GOD
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.structure = Product.PARENT
        self.instance.product_class = products.get_finished_class()


    def save(self):
        """
        Create/update a product object based on form data
        """
        if not self.is_valid():
            raise Exception('save_product() called on invalid form')

        product_data = self.cleaned_data

        if self.instance:
            product_data['instance'] = self.instance

        return products.save_finished(**product_data)


class UnfinishedForm(ProductForm):
    """
    A form specifically tailored to creating an Unfinished Blank product
    """
    pine_price = forms.DecimalField(label="Pine Price",
            min_value=0,
            decimal_places=2,
            max_digits=12,
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


    # Make the product_class field NOT REQUIRED, FOR THE LOVE OF GOD
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.structure = Product.PARENT
        self.instance.product_class = products.get_unfinished_class()


    def save(self):
        """
        Create/update a product object based on form data
        """
        if not self.is_valid():
            raise Exception('save_product() called on invalid form')

        product_data = self.cleaned_data

        if self.instance:
            product_data['instance'] = self.instance

        return products.save_unfinished(**product_data)


class InstructionsForm(ProductForm):
    """
    A form specifically tailored to creating Instructions product
    """
    pass

