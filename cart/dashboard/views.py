from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
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
StockRecord = get_model('partner', 'StockRecord')



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
    context_table_name = 'products'
    queryset = Product.browsable.filter(product_class__name='Unfinished Blanks')
    table_class = tables.UnfinishedTable
    template_name = 'dashboard/catalogue/product_unfinished.html'



class UnfinishedMixin():
    """
    Contain common functionality for create and update views
    """
    form_class = forms.UnfinishedForm
    queryset = Product.objects.filter(product_class__name='Unfinished Blanks')
    success_url = reverse_lazy('dashboard:catalogue-unfinished-list')
    template_name = 'dashboard/catalogue/product_unfinished_update.html'
    category_formset = ProductCategoryFormSet
    image_formset = ProductImageFormSet



class UnfinishedCreateView(generic.CreateView, UnfinishedMixin):
    """
    Create an unfinished blank
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formsets = {
            'category_formset': self.category_formset,
            'image_formset': self.image_formset,
        }
        self.product_class = ProductClass.objects.get(name='Unfinished Blanks')



class UnfinishedUpdateView(generic.UpdateView, UnfinishedMixin):
    """
    Update an unfinished blank
    """


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formsets = {
            'category_formset': self.category_formset,
            'image_formset': self.image_formset,
        }
        self.product_class = ProductClass.objects.get(name='Unfinished Blanks')


    def form_valid(self, form):
        """
        Save updates to, or create, the product
        """

        #TODO: process formsets!

        super().form_valid(form)


    def get_context_data(self, *args, **kwargs):
        """
        Override get_context_data to fix the page title
        """
        context = super().get_context_data(*args, **kwargs)

        # Add the product formsets
#        for ctx_name, formset_class in self.formsets.items():
#            if ctx_name not in context:
#                context[ctx_name] = formset_class(
#                    self.request.user,
#                    self.product_class)

        context['title'] = 'Add Unfinished Blank'

        return context


    def get_initial(self):
        """
        If there has been a product sent in, get its values and pre-populate
        the form
        """
        initial = {
            'title': self.object.title,
        }

        # Get the material variant pricing/sku details
        initial['pine_sku'], initial['pine_price'] = get_pine(self.object)
        initial['tupelo_sku'], initial['tupelo_price'] = get_tupelo(self.object)

        #TODO: implement feet pricing

#        formsets = {}
#
#        # Check the formsets for validity
#        for key, formset in self.formsets.items():
#            formsets[key] = formset(self.product_class,
#                   self.request.user,
#                   self.request.POST,
#                   self.request.FILES,
#                   instance=self.product)
#
#        self.formsets = formsets

        return initial


    def get_object(self):
        """
        Populate the existing object if one has been sent in
        """
        if 'pk' in self.kwargs:
            return Product.objects.get(pk=self.kwargs.get('pk'))

        return None


    def post(self, request, *arg, **kwargs):
        """
        Override post method to check the formsets' validity
        """

#        for key, formset in self.formsets:
#            if not formset.is_valid():
#                self.form_invalid(self, self.form)

        # Call the parent method to validate the main form
        super().post(request, *arg, **kwargs)

