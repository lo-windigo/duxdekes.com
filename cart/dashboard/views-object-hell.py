from django.core.urlresolvers import reverse
from django_tables2 import SingleTableView
from oscar.core.loading import get_class, get_model
from . import forms, tables

# Dynamically get the oscar models
Product = get_model('catalogue', 'Product')
ProductCreateUpdateView = get_class('dashboard.catalogue.views', 'ProductCreateUpdateView')


class UnfinishedListView(SingleTableView):
    """
    Dashboard view that lists existing unfinished blanks
    """
    template_name = 'dashboard/catalogue/product_unfinished.html'
    table_class = tables.UnfinishedTable
    context_table_name = 'products'
    queryset = Product.browsable.filter(product_class__name='Unfinished Blanks')



class UnfinishedCreateUpdateView(ProductCreateUpdateView):

    form_class = forms.UnfinishedForm


    def get_objects(self, queryset=None):
        """
        Override the get objects method to set the product class slug
        """
        kwargs = self.kwargs
        self.kwargs = kwargs.update({'product_class_slug': 'unfinished-blanks' })

        return super().get_objects(queryset)


    def get_success_url(self):
        """
        Return the pattern for the success state (just take us back to the
        product listing)
        """
        return reverse('dashboard:catalogue-unfinished-create')


