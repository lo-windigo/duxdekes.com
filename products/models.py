from django.db import models


class ProductCategory(models.Model):
    """
    A top-level product category
    """
    description = models.CharField('Name',
            max_length=300)
    hidden = models.BooleanField('Hide category?',
            default = False)
    explanation = models.TextField('Extra category information',
            blank=True)


    def __str__(self):
        return self.description



class ProductType(ProductCategory):
    """
    A sub-category of products
    """
    parent = models.ForeignKey(ProductCategory,
            related_name='+')



class Product(models.Model):
    """
    A generic product model that others can build on
    """
    description = models.CharField('Description',
            max_length=300)
    product_id = models.CharField('ID',
            max_length=30)
    base_price = models.DecimalField('Price',
            max_digits=9,
            decimal_places=2)
    hidden = models.BooleanField('Hide product?',
            default = False)
    category = models.ForeignKey(ProductType)

    class Meta:
        default_related_name = "products"


    def __str__(self):
        return self.description


    def get_absolute_url(self):
        pass



class Decoy(Product):
    pass


class Instruction(Product):
    pass


class FinishedDecoy(Decoy):
    pass


class UnfinishedDecoy(Decoy):
    MATERIALS = (
            ('OAK', 'Oak'),
            ('PINE', 'Pine')
            )

    materials = models.CharField('Material',
            max_length=10,
            choices=MATERIALS)

