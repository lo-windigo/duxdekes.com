from oscar.apps.catalogue.models import *  # noqa
from oscar.core.loading import get_model
from django.db import models
from duxdekes.util import products

StockRecord = get_model('partner', 'StockRecord')


class InstructionsProduct(Product):
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
#    description = models.TextField(blank=True,
#            null=True)
#    instructions_for = models.TextField(blank=True,
#            null=True)
#    author = models.CharField(max_length=128,
#            blank=True,
#            null=True)
#    product_code = models.CharField(max_length=64,
#            blank=True,
#            null=True)
#    isbn_13 = models.CharField(max_length=17,
#            blank=True,
#            null=True)
#    isbn_10 = models.CharField(max_length=13,
#            blank=True,
#            null=True)
#    pages = models.CharField(max_length=64,
#            blank=True,
#            null=True)
#    binding = models.CharField(max_length=64,
#            blank=True,
#            null=True)
#    size = models.CharField(max_length=64,
#            blank=True,
#            null=True)
#
#    def save(self, *args, **kwargs):
#        """
#        Save the model, and hook up a bunch of other Oscar-specific connections
#        """
#        self.product_class = products.get_instructions_class()
#        self.structure = Product.PARENT
#
#        # Save this model the ol' fashioned way
#        super().save(*args, **kwargs)

