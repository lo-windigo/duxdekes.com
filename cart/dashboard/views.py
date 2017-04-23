from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import base, edit
from django_tables2 import SingleTableMixin, SingleTableView
from oscar.core.loading import get_classes, get_model
from . import forms


# Dynamically get any oscar models/classes in use
ProductClass = get_model('catalogue', 'ProductClass')
Product = get_model('catalogue', 'Product')
ProductTable, CategoryTable \
    = get_classes('dashboard.catalogue.tables',
                  ('ProductTable', 'CategoryTable'))
ProductCategoryFormSet, ProductImageFormSet \
    = get_classes('dashboard.catalogue.forms',
        (
            'ProductCategoryFormSet',
            'ProductImageFormSet',
        ))


class CustomCreateUpdateMixin(generic.TemplateView):
    """
    """
    def get(self):
        pass


    def post(self):
        pass



class BauerListView(SingleTableView):
    pass


class FinishedListView(SingleTableView):
    template_name = 'dashboard/catalogue/product_finished.html'
    table_class = ProductTable
    context_table_name = 'products'
    queryset = Product.browsable.filter(product_class__name='Finished Carvings')


class InstructionListView(SingleTableView):
    pass


class UnfinishedListView(SingleTableView):
    """
    Dashboard view that lists existing unfinished blanks
    """
    template_name = 'dashboard/catalogue/product_unfinished.html'
    table_class = ProductTable
    context_table_name = 'products'
    queryset = Product.browsable.filter(product_class__name='Unfinished Blanks')



class UnfinishedCreateUpdateView(edit.FormMixin, base.TemplateView):
    """
    Create/update an unfinished blank
    """
    template_name = 'dashboard/catalogue/product_unfinished_update.html'
    form_class = forms.UnfinishedForm
    success_url = 'catalogue-unfinished'


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_class = ProductClass.objects.get(name='Unfinished Blanks')


    def form_valid(self):
        """
        Save updates to, or create, the product
        """
        pass


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create the product formsets
        categories = ProductCategoryFormSet(
            self.request.user,
            self.product_class)
        image = ProductImageFormSet(
            self.request.user,
            self.product_class)
        context['title'] = 'Add Unfinished Blank'
        context['category_formset'] = categories
        context['image_formset'] = image
        return context

