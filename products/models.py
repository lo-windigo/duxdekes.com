from django.db import models
from django.shortcuts import reverse


class ProductCategory(models.Model):
    """
    A category of similar products that are displayed together in a product
    listing
    """
    UNFINISHED = 'u'
    FINISHED = 'f'
    INSTRUCTION = 'i'
    MATERIAL = 'm'
    PRODUCT_TYPE = (
            (UNFINISHED, 'Unfinished Blanks'),
            (FINISHED, 'Finished Decoys'),
            (INSTRUCTION, 'Instructions'),
            (MATERIAL, 'Materials'),
            (None, 'Unset'),
            )

    category_type = models.CharField('Type',
            choices=PRODUCT_TYPE,
            default=UNFINISHED,
            max_length=1)
    description = models.CharField('Name',
            max_length=300)
    hidden = models.BooleanField('Hide category?',
            default = False)
    explanation = models.TextField('Extra category information',
            blank=True,
            null=True)
    slug = models.SlugField(
            unique=True)
    #TODO: Would this be better as a file upload field?
    template = models.CharField('Custom template',
            max_length=300,
            blank=True,
            null=True)


    class Meta:
        verbose_name_plural = "Product Categories"


    def __str__(self):
        return self.description


    def get_absolute_url(self):
        return reverse('listing', self.slug)



class Product(models.Model):
    """
    A generic product model that others can build on
    """
    description = models.CharField('Description',
            max_length=300)
    product_id = models.CharField('ID',
            max_length=30,
            blank = True,
            null = True)
    base_price = models.DecimalField('Price',
            max_digits=9,
            decimal_places=2)
    hidden = models.BooleanField('Hide product?',
            default = False)
    category = models.ForeignKey(ProductCategory,
            blank = True,
            null = True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        default_related_name = "products"


    def __str__(self):
        return self.description


    def get_absolute_url(self):
        pass

