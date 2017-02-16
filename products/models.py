from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify


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
        return "({}) {}".format(self.get_category_type_display(), self.description)


    def get_absolute_url(self):
        return reverse('listing', args=[self.slug])


    def save(self, *args, **kwargs):

        # Create a slug field if none is present
        if not self.id and not self.slug:
            self.slug = slugify(self.description)

        super(ProductCategory, self).save(*args, **kwargs)



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



class Picture(models.Model):
    """
    A product image
    """
    description = models.CharField('Name',
            blank=True,
            max_length=300)
    image = models.ImageField('Picture',
            upload_to='products/')
    product = models.ForeignKey(Product,
            on_delete=models.CASCADE)

    def get_absolute_url(self):
        return self.image.url



class UnfinishedDecoy(Product):
    """
    An unfinished decoy, which can be available in multiple materials
    """
    pine_price = models.DecimalField('Price of Pine',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)
    feet_price = models.BooleanField('Optional Feet Fee',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)
    tupelo_price = models.BooleanField('Price of Tupelo',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)



class Instructions(Product):
    """
    A set of instructions for painting your own decoy
    """
    price = models.DecimalField('Instructions only price',
            max_digits=9,
            decimal_places=2)
    blank_price = models.BooleanField('Price with Blank',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)
    matching_blank = models.ForeignKey(Product)



class FinishedDecoy(Product):
    """
    An unfinished decoy, which can be available in multiple materials
    """
    pine_price = models.DecimalField('Price of Pine',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)
    feet_price = models.BooleanField('Optional Feet Fee',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)
    tupelo_price = models.BooleanField('Price of Tupelo',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)

