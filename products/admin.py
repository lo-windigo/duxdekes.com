from django.contrib import admin
from .models import ProductCategory, ProductType, Instruction, UnfinishedDecoy, FinishedDecoy

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Instruction)
admin.site.register(UnfinishedDecoy)
admin.site.register(FinishedDecoy)
