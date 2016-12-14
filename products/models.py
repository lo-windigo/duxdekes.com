from django.db import models


class ProductCategory(models.Model):
    description = models.CharField('Name',
            max_length=300)
    hidden = models.BooleanField('Hide category?',
            default = False)
    explanation = model.TextField('Extra category information',
            blank=True)


class ProductType(ProductCategory):
    parent = models.ForeignKey(ProductCategory)


class Product(models.Model):
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


class Decoy(Product):
    pass

