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


#@admin.register(models.Product)
#class ProductAdmin(admin.ModelAdmin):
#    inlines = [PictureInline,]
#    ordering = ['description']
#    list_filter = ('category__category_type',)
#    view_on_site = False


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('hidden', 'category', )
    inlines = [ PictureInline, ]
    ordering = ['description']
    actions = [
            'convert_to_finished',
            'convert_to_instructions',
            'convert_to_unfinished',
            ]


    def convert_to_finished(self, request, queryset):
        for product in queryset:
            models.FinishedCarving.convert_from_product(product)

    convert_to_finished.short_description = 'Convert to "Finished Carving"'


    def convert_to_instructions(self, request, queryset):
        for product in queryset:
            models.Instructions.convert_from_product(product)

    convert_to_instructions.short_description = 'Convert to "Instructions"'


    def convert_to_unfinished(self, request, queryset):
        for product in queryset:
            models.UnfinishedBlank.convert_from_product(product)

    convert_to_unfinished.short_description = 'Convert to "Unfinished Blank"'

admin.site.register(models.Instructions, ProductAdmin)
admin.site.register(models.FinishedCarving, ProductAdmin)
admin.site.register(models.UnfinishedBlank, ProductAdmin)

