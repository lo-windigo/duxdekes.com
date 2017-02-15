from django.contrib import admin
from . import models


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_filter = ('category_type',)
    ordering = ['description']
    prepopulated_fields = {"slug": ("description",)}
    radio_fields = {"category_type": admin.HORIZONTAL}


class PictureInline(admin.TabularInline):
    model = models.Picture


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PictureInline,]
    ordering = ['description']
    list_filter = ('category__category_type',)
    view_on_site = False


admin.register(models.Picture)

