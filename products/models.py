from django.db import models


class ProductCategory(models.Model):
    """
    A top-level product category
    """
    description = models.CharField('Name',
            max_length=300)
    hidden = models.BooleanField('Hide category?',
            default = False)
    explanation = model.TextField('Extra category information',
            blank=True)


class ProductType(ProductCategory):
    """
    A sub-category of products
    """
    parent = models.ForeignKey(ProductCategory)


class Product(models.Model):
    """
    A generic product model that others can build on
    """
    description = models.CharField('Description',
            max_length=300)
    product_id = models.CharField('ID',
            max_length=30)
    base_price = models.DecimalField('Price',
            decimal_places=2)
    hidden = models.BooleanField('Hide product?',
            default = False)
    category = models.ForeignKey(ProductType)


class Decoy(Product):
    pass


class Instruction(Product):
    pass


class FinishedDecoy(Decoy):
    pass


class UnfinishedDecoy(Decoy):
    MATERIALS = (
            (OAK, 'Oak')
            (PINE, 'Pine')
            )

    materials = model.CharField('Material',
            choices=MATERIALS)

