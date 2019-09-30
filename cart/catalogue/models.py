from oscar.apps.catalogue.abstract_models import \
        AbstractProductClass, AbstractProduct
from oscar.core.loading import get_model
from django.db import models
from .util import product_class, products


class ProductClass(AbstractProductClass):
    """
    Override the product class save method to add required attributes
    """

    def save(self, *args, **kwargs):
        """
        Save the object as usual, and then call the utility function to add
        required attributes to all product classes
        """
        super().save()

        # Make sure ALL product classes have the right attributes
        product_class.make_class_attributes()


class Product(AbstractProduct):
    """
    Add an "active" flag to the product class
    """
    is_active = models.BooleanField(default=True)


# Import the remaining Oscar models
from oscar.apps.catalogue.models import *  # noqa
StockRecord = get_model('partner', 'StockRecord')


class InstructionsProduct(Product):
    """
    A product specifically designed to be used for special instructions
    """
    TITLE_ALONE = '{} Painting Kit'
    TITLE_WITH_BLANK = '{} Painting Kit & {} blank'
    SKU_WITH_BLANK_UPC = '{}B'

    sku = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=12,
            decimal_places=2)
    price_with_blank = models.DecimalField(max_digits=12,
            decimal_places=2,
            blank=True,
            null=True)
    blank = models.ForeignKey(Product,
            related_name='paired_blank',
            blank=True,
            null=True)
    alone_stock = models.ForeignKey(StockRecord,
            related_name='alone',
            blank=True,
            null=True)
    with_blank_stock = models.ForeignKey(StockRecord,
            related_name='with_blank',
            blank=True,
            null=True)

    def save(self, *args, **kwargs):
        """
        Save the model, and hook up a bunch of other Oscar-specific connections
        """
        self.product_class = products.get_instructions_class()
        self.structure = Product.PARENT

        # Save this model the ol' fashioned way
        super().save(*args, **kwargs)

        # Stock records and child products for a la carte instructions
        new_alone = not self.alone_stock
        if new_alone:
            alone = Product()
            alone.parent = self
            alone.structure = Product.CHILD

            alone_stock = StockRecord()
            alone_stock.partner = products.get_partner()
        else:
            alone_stock = self.alone_stock
            alone = self.alone_stock.product
        
        alone.title = self.TITLE_ALONE.format(self.title)
        #alone.upc = self.sku
        alone.save()

        if new_alone:
            alone_stock.product = alone

        alone_stock.partner_sku = self.sku
        alone_stock.price_excl_tax = self.price
        alone_stock.save()

        self.alone_stock = alone_stock

        # Stock records and child products for instructions with blank
        if self.blank and self.price_with_blank:
            new_w_blank = not self.with_blank_stock
            if new_w_blank:
                with_blank = Product()
                with_blank.parent = self
                with_blank.structure = Product.CHILD

                with_blank_stock = StockRecord()
                with_blank_stock.partner = products.get_partner()
            else:
                with_blank_stock = self.with_blank_stock
                with_blank = with_blank_stock.product
            
            with_blank.title = self.TITLE_WITH_BLANK.format(self.title,
                    self.blank.title)
            #with_blank.upc = self.SKU_WITH_BLANK.format(self.sku)
            with_blank.save()

            if new_w_blank:
                with_blank_stock.product = with_blank

            with_blank_stock.partner_sku = \
                self.SKU_WITH_BLANK_UPC.format(self.sku)
            with_blank_stock.price_excl_tax = self.price_with_blank
            with_blank_stock.save()

            self.with_blank_stock = with_blank_stock
        else:
            new_w_blank = False

        # If either of these have been added, we need to re-save the model to
        # point to the new StockRecord objects
        if new_alone or new_w_blank:
            super().save(*args, **kwargs)



#class BookInstructionsProduct(Product):
#    """
#    Override the usual product model to include extra descriptive content
#    """
#    extra_content = models.ForeignKey(FlatPage,
#            blank = True,
#            null = True)

