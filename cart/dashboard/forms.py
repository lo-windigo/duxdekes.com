from cart.catalogue.util import products
from cart.shipping.models import Box
from django import forms
from oscar.core.loading import get_class, get_model
from oscar.apps.dashboard.catalogue.forms import ProductForm as OscarProductForm

InstructionsProduct = get_model('catalogue', 'InstructionsProduct')
Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')

PRIMARY_MODEL_FIELDS=('title', 'upc')


def _attr_box_entity_field(attribute):
    return forms.ModelChoiceField(label=attribute.name,
            queryset=Box.objects.all(),
            required=attribute.required)


class ProductForm(OscarProductForm):
    """
    A generic product form, containing common fields
    """

    def __init__(self, *args, **kwargs):
        """
        Override the default "required" attribute of the form fields
        """
        super().__init__(*args, **kwargs)

        for field in PRIMARY_MODEL_FIELDS:
            self.fields[field].required = True

        # Assign a special handler for entity fields
        self.FIELD_FACTORIES["entity"] = _attr_box_entity_field


    class Meta:
        """
        Meta data for this model form
        """
        model = Product
        fields = PRIMARY_MODEL_FIELDS



class FinishedForm(ProductForm):
    """
    A form specifically tailored to creating a finished decoy
    """
    price = forms.DecimalField(label="Price",
            min_value=0,
            decimal_places=2,
            max_digits=12)


    # Make the product_class field NOT REQUIRED, FOR THE LOVE OF GOD
    def __init__(self, *args, **kwargs):
        super().__init__(products.get_finished_class(), *args, **kwargs)


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
        super().__init__(products.get_unfinished_class(), *args, **kwargs)
        self.instance.structure = Product.PARENT


    def save(self):
        """
        Create/update a product object based on form data
        """
        if not self.is_valid():
            raise Exception('save() called on invalid form')

        product_data = self.cleaned_data

        if self.instance:
            product_data['instance'] = self.instance

        return products.save_unfinished(**product_data)


class InstructionsForm(forms.ModelForm):
    """
    A form specifically tailored to creating Instructions product
    """
    blank = forms.ModelChoiceField(label="Optional Blank",
            queryset=Product.objects.filter(
                product_class=products.get_unfinished_class()),
            required=False,
            empty_label='No blank')


    # Make the product_class field NOT REQUIRED, FOR THE LOVE OF GOD
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.product_class = products.get_instructions_class()

    class Meta:
        model = InstructionsProduct
        fields = ['title', 'sku', 'price', 'price_with_blank', 'blank']

