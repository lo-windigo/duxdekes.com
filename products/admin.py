from django.contrib import admin
from .models import ProductCategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_filter = ('category_type',)
    ordering = ['description']
    prepopulated_fields = {"slug": ("description",)}
    radio_fields = {"category_type": admin.HORIZONTAL}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ['description']
    list_filter = ('category__category_type',)
    view_on_site = False

