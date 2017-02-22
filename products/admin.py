from django.contrib import admin
from . import models


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_filter = ('category_type',)
    ordering = ['description']
    prepopulated_fields = {"slug": ("description",)}
    radio_fields = {"category_type": admin.HORIZONTAL}


    def convert_to_finished(self, request, queryset):
        for product in queryset:
            models.FinishedDecoy.convert_from_product(product)

    convert_to_finished.short_description = 'Convert to "Finished Decoy"'


    def convert_to_instructions(self, request, queryset):
        for product in queryset:
            models.Instructions.convert_from_product(product)

    convert_to_unfinished.short_description = 'Convert to "Unfinished Decoy"'


    def convert_to_unfinished(self, request, queryset):
        for product in queryset:
            models.UnfinishedDecoy.convert_from_product(product)

    convert_to_unfinished.short_description = 'Convert to "Unfinished Decoy"'



class PictureInline(admin.TabularInline):
    model = models.Picture


#@admin.register(models.Product)
#class ProductAdmin(admin.ModelAdmin):
#    inlines = [PictureInline,]
#    ordering = ['description']
#    list_filter = ('category__category_type',)
#    view_on_site = False


class ProductAdmin(admin.ModelAdmin):
    inlines = [PictureInline,]
    ordering = ['description']

admin.site.register(models.Instructions, ProductAdmin)
admin.site.register(models.FinishedDecoy, ProductAdmin)
admin.site.register(models.UnfinishedDecoy, ProductAdmin)


