
from django.db import models
from oscar.apps.catalogue.managers import ProductQuerySet as OscarProductQuerySet


class ProductQuerySet(OscarProductQuerySet):
    """
    Override the default ProductQuerySet to ignore products with an is_active
    flag set to false
    """
    def browsable(self):
        """
        Excludes non-active products.
        """
        return super().browsable().filter(is_active=True)


"""
Copy the rest of the Oscar classes below (they pull things in directly from
classes defined in the same file)
"""


class ProductManager(models.Manager):
    """
    Uses ProductQuerySet and proxies its methods to allow chaining

    Once Django 1.7 lands, this class can probably be removed:
    https://docs.djangoproject.com/en/dev/releases/1.7/#calling-custom-queryset-methods-from-the-manager  # noqa
    """

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def browsable(self):
        return self.get_queryset().browsable()

    def base_queryset(self):
        return self.get_queryset().base_queryset()


class BrowsableProductManager(ProductManager):
    """
    Excludes non-canonical products

    Could be deprecated after Oscar 0.7 is released
    """

    def get_queryset(self):
        return super(BrowsableProductManager, self).get_queryset().browsable()
