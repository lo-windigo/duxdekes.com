from cart.catalogue.util import products
from cart.shipping.models import Box
from django import forms
from oscar.core.loading import get_model
from oscar.apps.dashboard.catalogue.forms import ProductForm as OscarProductForm

InstructionsProduct = get_model('catalogue', 'InstructionsProduct')
Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')

PRIMARY_MODEL_FIELDS = ('title', 'upc')


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

        # Assign a special handler for entity fields
        self.FIELD_FACTORIES["entity"] = _attr_box_entity_field

        super().__init__(*args, **kwargs)

        # Set the primary fields as required
        for field in PRIMARY_MODEL_FIELDS:
            if field in self.fields:
                self.fields[field].required = True

    class Meta:
        model = Product
        fields = PRIMARY_MODEL_FIELDS + ('is_active',)


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

    def save(self, commit=True):
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

    def save(self, commit=True):
        """
        Create/update a product object based on form data
        """
        if not self.is_valid():
            raise Exception('save() called on invalid form')

        product_data = self.cleaned_data

        if self.instance:
            product_data['instance'] = self.instance

        return products.save_unfinished(**product_data)


class InstructionsForm(ProductForm):
    """
    A form specifically tailored to creating Instructions product
    """
    blank = forms.ModelChoiceField(label="Optional Blank",
                                   queryset=Product.objects.filter(
                                       product_class=products.get_unfinished_class()
                                   ).order_by('title'),
                                   required=False,
                                   empty_label='No blank')

    # Make the product_class field NOT REQUIRED, FOR THE LOVE OF GOD
    def __init__(self, *args, **kwargs):
        klass = products.get_instructions_class()
        super().__init__(klass, *args, **kwargs)
        self.instance.product_class = klass

    class Meta:
        model = InstructionsProduct
        fields = ['title', 'sku', 'price', 'is_active', 'price_with_blank', 'blank']

