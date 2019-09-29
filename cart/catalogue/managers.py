
from django.db import models


class ActiveProductManager(models.Manager):
    """
    A manager that only shows active products
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
