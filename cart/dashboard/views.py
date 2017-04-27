from django.core.urlresolvers import reverse
from django.views import generic
from django_tables2 import SingleTableMixin, SingleTableView
from oscar.core.loading import get_classes, get_model
from . import forms, tables
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
    table_class = tables.UnfinishedTable
    context_table_name = 'products'
    queryset = Product.browsable.filter(product_class__name='Unfinished Blanks')



class UnfinishedCreateUpdateView(generic.FormView):
    """
    Create/update an unfinished blank
    """
    template_name = 'dashboard/catalogue/product_unfinished_update.html'
    form_class = forms.UnfinishedForm
    category_formset = ProductCategoryFormSet
    image_formset = ProductImageFormSet


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.formsets = {'category_formset': self.category_formset,
                'image_formset': self.image_formset}
        self.product_class = ProductClass.objects.get(name='Unfinished Blanks')

        # If there has been a product sent in, get its values and pre-populate
        # the form
        # TODO
        if 'unfinished_pk' in kwargs:
            self.initial = {}


    def form_valid(self, form):
        """
        Save updates to, or create, the product
        """
        form.save_product()
        super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the product formsets
        for ctx_name, formset_class in self.formsets.items():
            if ctx_name not in context:
                context[ctx_name] = formset_class(
                    self.request.user,
                    self.product_class)

        context['title'] = 'Add Unfinished Blank'

        return context


    def get_success_url(self):
        """
        Return the pattern for the success state (just take us back to the
        product listing)
        """
        return reverse('dashboard:catalogue-unfinished-create')


    def post(self, request, *arg, **kwargs):
        """
        Override post method to check the formsets' validity
        """

        # Check the formsets for validity
        for formset in self.formsets:
            if not formset.is_valid():
                self.form_invalid(self, self.form)

        # Call the parent method to validate the main form
        super().post(request, *arg, **kwargs)

