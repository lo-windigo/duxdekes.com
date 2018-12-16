from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django_tables2 import SingleTableMixin, SingleTableView
from oscar.core.loading import get_class, get_classes, get_model
from . import forms, tables
from duxdekes.util import products


# Dynamically get any oscar models/classes in use
InstructionsProduct = get_model('catalogue', 'InstructionsProduct')
ProductTable, CategoryTable \
    = get_classes('dashboard.catalogue.tables',
                  ('ProductTable', 'CategoryTable'))
ProductCategoryFormSet, ProductImageFormSet, ProductAttributesFormSet \
    = get_classes('dashboard.catalogue.forms',
        (
            'ProductCategoryFormSet',
            'ProductImageFormSet',
            'ProductAttributesFormSet',
        ))
ProductDeleteView = get_class('dashboard.catalogue.views', 'ProductDeleteView')
Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')
StockRecord = get_model('partner', 'StockRecord')


class ProductMixin():
    """
    A basic mixin used for all of our custom products
    """
    cached_product_class = False
    category_formset = ProductCategoryFormSet
    image_formset = ProductImageFormSet
    #product_attributes_formset = ProductAttributesFormSet


    def __init__(self, *args, **kwargs):
        """
        Override to set up the formsets dictionary
        """
        super().__init__(*args, **kwargs)

        self.formsets = {
            #'product_attributes_formset': self.product_attributes_formset,
            'category_formset': self.category_formset,
            'image_formset': self.image_formset,
        }
        self.queryset = Product.objects.filter(product_class=self.get_product_class())


    def get_context_data(self, *args, **kwargs):
        """
        Override get_context_data to fix the page title
        """
        context = super().get_context_data(*args, **kwargs)

        # Set the product title, if set
        if self.view_title:
            context['title'] = self.view_title

        # Add the product formsets
        instance = None
        if self.object:
            instance = self.object

        for ctx_name, formset_class in self.formsets.items():
            if ctx_name not in context:
                context[ctx_name] = formset_class(self.product_class,
                    self.request.user,
                    instance=instance)

        if not 'product_class' in context:
            context['product_class'] = self.product_class

        return context


    def post(self, request, *args, **kwargs):
        """
        Override post method to save formsets
        """

        initial_response = super().post(request, *args, **kwargs)

        # check for failure of initial form
        if not isinstance(initial_response, HttpResponseRedirect):
            return initial_response

        # Process formsets
        formsets = {}

        for key, formset in self.formsets.items():
            formsets[key] = formset(self.product_class,
                   request.user,
                   request.POST,
                   request.FILES,
                   instance=self.object)

        if all([formset.is_valid() for formset in formsets.values()]):
            for formset in formsets.values():
                formset.save()

            # All is well - return success!
            messages.success(request,
                    getattr(self, 'success_message',
                        'Product successfully saved.'),
                    extra_tags="safe noicon")
            return initial_response

        else:
            return self.form_invalid(self.get_form())


    @property
    def product_class(self):
        """
        Must be implemented on each extending mixin!
        """
        if not self.cached_product_class:
            try:
                self.cached_product_class = self.get_product_class()
            except:
                raise NotImplemented('No product class defined!')

        return self.cached_product_class



class FinishedListView(SingleTableView):
    """
    Display a list of Finished Decoys
    """
    template_name = 'dashboard/catalogue/product_finished.html'
    table_class = tables.FinishedTable
    context_table_name = 'products'
    queryset = Product.browsable.filter(product_class=products.get_finished_class())


    def get_table(self, **kwargs):
        """
        Set the table caption by overriding the parent method
        """
        table = super().get_table(**kwargs)
        table.caption = 'Finished Decoys'
        return table



class FinishedMixin(ProductMixin):
    """
    Contain common functionality for create and update views
    """
    form_class = forms.FinishedForm
    success_url = reverse_lazy('dashboard:catalogue-finished-list')
    success_message = 'Decoy successfully saved'
    template_name = 'dashboard/catalogue/product_finished_update.html'


    def get_product_class(self):
        """
        Return the product class associated with this type of product
        """
        return products.get_finished_class()



class FinishedCreateView(FinishedMixin, generic.CreateView):
    """
    Create an finished decoy
    """
    view_title = 'Add Finished Decoy'



class FinishedUpdateView(FinishedMixin, generic.UpdateView):
    """
    Update an finished decoy
    """
    view_title = 'Change Finished Decoy'


    def get_initial(self):
        """
        If there has been a product sent in, get its values and pre-populate
        the form
        """
        initial = super().get_initial()

        # Set the price from the related stock record
        try:
            stock = StockRecord.objects.get(product=self.object)
            initial['price'] = stock.price_excl_tax
        except:
            pass

        # Get the pricing/sku details
        return initial


    def get_object(self):
        """
        Populate the existing object if one has been sent in
        """
        if 'pk' in self.kwargs:
            return Product.objects.get(pk=self.kwargs.get('pk'))

        return None



class FinishedDeleteView(ProductDeleteView):
    """
    Override the get_success_url method of the generic ProductDeleteView to send us
    back to the finished decoy section
    """
    view_title = 'Remove Finished Decoy'


    def get_success_url(self):
        """
        When deleting child products, this view redirects to editing the
        parent product. When deleting any other product, it redirects to the
        product list view.
        """
        if self.object.is_child:
            msg = _("Deleted product variant '%s'") % self.object.get_title()
            messages.success(self.request, msg)
            return reverse(
                'dashboard:catalogue-finished',
                kwargs={'pk': self.object.parent_id})
        else:
            msg = _("Deleted product '%s'") % self.object.title
            messages.success(self.request, msg)
            return reverse('dashboard:catalogue-finished-list')


class InstructionsListView(SingleTableView):
    template_name = 'dashboard/catalogue/product_instructions.html'
    table_class = tables.InstructionsTable
    context_table_name = 'products'
    model = InstructionsProduct

    def get_table(self, **kwargs):
        """
        Set the table caption by overriding the parent method
        """
        table = super().get_table(**kwargs)
        table.caption = 'Instructions'
        return table


class InstructionsMixin(ProductMixin):
    """
    Contain common functionality for create and update views
    """
    form_class = forms.InstructionsForm
    model = InstructionsProduct
    success_url = reverse_lazy('dashboard:catalogue-instructions-list')
    success_message = 'Instructions successfully saved'
    template_name = 'dashboard/catalogue/product_instructions_update.html'


    def __init__(self, *args, **kwargs):
        """
        We don't need no stinkin' queryset
        """
        super().__init__(*args, **kwargs)
        del self.queryset


    def get_product_class(self):
        """
        Return the product class associated with this type of product
        """
        return products.get_instructions_class()



class InstructionsCreateView(InstructionsMixin, generic.CreateView):
    """
    Create an instruction
    """
    view_title = 'Add Instructions'



class InstructionsUpdateView(InstructionsMixin, generic.UpdateView):
    """
    Update an instruction product
    """
    view_title = 'Change Instructions'



class InstructionsDeleteView(ProductDeleteView):
    """
    Override the get_success_url method of the generic ProductDeleteView to send us
    back to the instruction section
    """
    def get_success_url(self):
        """
        When deleting child products, this view redirects to editing the
        parent product. When deleting any other product, it redirects to the
        product list view.
        """
        if self.object.is_child:
            msg = _("Deleted product variant '%s'") % self.object.get_title()
            messages.success(self.request, msg)
            return reverse(
                'dashboard:catalogue-instructions',
                kwargs={'pk': self.object.parent_id})
        else:
            msg = _("Deleted product '%s'") % self.object.title
            messages.success(self.request, msg)
            return reverse('dashboard:catalogue-instructions-list')



class UnfinishedListView(SingleTableView):
    """
    Dashboard view that lists existing finished decoys
    """
    context_table_name = 'products'
    queryset = Product.browsable.filter(product_class=products.get_unfinished_class())
    table_class = tables.UnfinishedTable
    template_name = 'dashboard/catalogue/product_unfinished.html'


    def get_table(self, **kwargs):
        """
        Set the table caption by overriding the parent method
        """
        table = super().get_table(**kwargs)
        table.caption = 'Unfinished Blanks'
        return table



class UnfinishedMixin(ProductMixin):
    """
    Contain common functionality for create and update views
    """
    form_class = forms.UnfinishedForm
    #queryset = Product.objects.filter(product_class=products.get_unfinished_class())
    success_url = reverse_lazy('dashboard:catalogue-unfinished-list')
    success_message = 'Blank successfully saved'
    template_name = 'dashboard/catalogue/product_unfinished_update.html'


    def get_product_class(self):
        """
        Return the product class associated with this type of product
        """
        return products.get_unfinished_class()



class UnfinishedCreateView(UnfinishedMixin, generic.CreateView):
    """
    Create an unfinished blank
    """
    view_title = 'Add Unfinished Blank'



class UnfinishedUpdateView(UnfinishedMixin, generic.UpdateView):
    """
    Update an unfinished blank
    """
    view_title = 'Change Unfinished Blank'

    def get_initial(self):
        """
        If there has been a product sent in, get its values and pre-populate
        the form
        """
        initial = {
            'title': self.object.title,
        }

        # Get the material variant pricing/sku details
        pine = products.get_pine(self.object)
        pine_feet = products.get_pine_feet(self.object)
        tupelo = products.get_tupelo(self.object)
        tupelo_feet = products.get_tupelo_feet(self.object)

        # Populate the price fields
        if pine:
            initial['pine_price'] = pine.price_excl_tax

            if pine_feet:
                initial['feet_price'] = pine_feet.price_excl_tax - pine.price_excl_tax

        if tupelo:
            initial['tupelo_price'] = tupelo.price_excl_tax

            if tupelo_feet and 'feet_price' not in initial:
                initial['feet_price'] = tupelo_feet.price_excl_tax - tupelo.price_excl_tax

        return initial


    def get_object(self):
        """
        Populate the existing object if one has been sent in
        """
        if 'pk' in self.kwargs:
            return Product.objects.get(pk=self.kwargs.get('pk'))

        return None



class UnfinishedDeleteView(ProductDeleteView):
    """
    Override the get_success_url method of the generic ProductDeleteView to send us
    back to the unfinished decoy section
    """
    def get_success_url(self):
        """
        When deleting child products, this view redirects to editing the
        parent product. When deleting any other product, it redirects to the
        product list view.
        """
        if self.object.is_child:
            msg = _("Deleted product variant '%s'") % self.object.get_title()
            messages.success(self.request, msg)
            return reverse(
                'dashboard:catalogue-unfinished',
                kwargs={'pk': self.object.parent_id})
        else:
            msg = _("Deleted product '%s'") % self.object.title
            messages.success(self.request, msg)
            return reverse('dashboard:catalogue-unfinished-list')

