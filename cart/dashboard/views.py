from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import base, edit
from django_tables2 import SingleTableMixin, SingleTableView
from oscar.core.loading import get_classes, get_model
from . import forms
from duxdekes.util import products


# Dynamically get any oscar models/classes in use
ProductTable, CategoryTable \
    = get_classes('dashboard.catalogue.tables',
                  ('ProductTable', 'CategoryTable'))
ProductCategoryFormSet, ProductImageFormSet \
    = get_classes('dashboard.catalogue.forms',
        (
            'ProductCategoryFormSet',
            'ProductImageFormSet',
        ))
Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')


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



class UnfinishedCreateUpdateView(edit.FormView):
    """
    Create/update an unfinished blank
    """
    template_name = 'dashboard/catalogue/product_unfinished_update.html'
    form_class = forms.UnfinishedForm
    success_url = '/dashboard/unfinished/'
    category_formset = ProductCategoryFormSet
    image_formset = ProductImageFormSet


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formsets = {'category_formset': self.category_formset,
                'image_formset': self.image_formset}
        self.product_class = ProductClass.objects.get(name='Unfinished Blanks')


    def form_valid(self, form):
        """
        Save updates to, or create, the product
        """
        form.save_product()
        super().form_valid(form)


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

