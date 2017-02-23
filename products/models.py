from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from sorl.thumbnail import ImageField

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
            (FINISHED, 'Finished Carving'),
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
    hidden = models.BooleanField('Hidden',
            default = False)
    category = models.ForeignKey(ProductCategory,
            blank = True,
            null = True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        default_related_name = "products"


    def __str__(self):
        return self.description


    @classmethod
    def convert_from_product(cls, product):
        attributes = {}
        parent_link_field = cls._meta.parents.get(product.__class__, None)
        attributes[parent_link_field.name] = product

        for field in product._meta.fields:
            attributes[field.name] = getattr(product, field.name)

        new_object = cls(**attributes)
        new_object.save()
        # Don't delete old object - turns out it gets linked to. o_O
        #product.delete()



class Picture(models.Model):
    """
    A product image
    """
    description = models.CharField('Name',
            blank=True,
            max_length=300)
    image = ImageField('Picture',
            upload_to='products/')
    product = models.ForeignKey(Product,
            on_delete=models.CASCADE)

    def get_absolute_url(self):
        return self.image.url



class UnfinishedBlank(Product):
    """
    An unfinished decoy, which can be available in multiple materials
    """
    pine_price = models.DecimalField('Price of Pine',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)
    feet_price = models.DecimalField('Optional Feet Fee',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)
    tupelo_price = models.DecimalField('Price of Tupelo',
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
            decimal_places=2,
            blank=True,
            null=True)
    blank_price = models.DecimalField('Price with Blank',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)
    matching_blank = models.ForeignKey(UnfinishedBlank,
            blank=True,
            null=True)


    class Meta:
        verbose_name_plural = "Instructions"



class FinishedCarving(Product):
    """
    A painted decoy
    """
    price = models.DecimalField('Price',
            max_digits=9,
            decimal_places=2,
            blank=True,
            null=True)

