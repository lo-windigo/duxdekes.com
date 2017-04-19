from django import forms


class ProductForm(forms.Form):
    """
    A generic product form, containing common fields
    """
    description = forms.CharField(label="Product Description",
            max_length=200)
    image = forms.ImageField(required=False)


class UnfinishedForm(ProductForm):
    """
    A form specifically tailored to creating an Unfinished Blank product
    """
    pine_id = forms.CharField(label="Pine ID",
            max_length=64)
    pine_price = forms.Field(label="Pine Price",
            max_length=200)


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

