from django.core.urlresolvers import reverse
from django.views import generic
from django_tables2 import SingleTableMixin, SingleTableView
from oscar.core.loading import get_classes, get_model


# Dynamically get the Product class
Product = get_model('catalogue', 'Product')
ProductTable, CategoryTable \
    = get_classes('dashboard.catalogue.tables',
                  ('ProductTable', 'CategoryTable'))
(ProductForm,
ProductCategoryFormSet,
ProductImageFormSet,) = get_classes('dashboard.catalogue.forms',
        (
            'ProductForm',
            'ProductCategoryFormSet',
            'ProductImageFormSet',
        ))
(ProductCreateUpdateView,) = get_classes('dashboard.catalogue.views',
        ( 'ProductCreateUpdateView', ))


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


class UnfinishedCreateRedirectView(generic.RedirectView):
    permanent = True
    query_string = False

    def get_redirect_url(self, **kwargs):
        return reverse('dashboard:catalogue-unfinished-create',
            kwargs={'product_class_slug': 'unfinished-blanks'})


class UnfinishedCreateUpdateView(ProductCreateUpdateView):
    """
    Dashboard view that is can both create and update products of all kinds.
    It can be used in three different ways, each of them with a unique URL
    pattern:
    - When creating a new standalone product, this view is called with the
      desired product class
    - When editing an existing product, this view is called with the product's
      primary key. If the product is a child product, the template considerably
      reduces the available form fields.
    - When creating a new child product, this view is called with the parent's
      primary key.

    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/catalogue/product_unfinished_update.html'
    model = Product
    context_object_name = 'product'

    form_class = ProductForm
    category_formset = ProductCategoryFormSet
    image_formset = ProductImageFormSet

