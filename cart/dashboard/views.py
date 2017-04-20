from django_tables2 import SingleTableMixin, SingleTableView
from oscar.core.loading import get_classes, get_model


# Dynamically get the Product class
Product = get_model('catalogue', 'Product')
ProductTable, CategoryTable \
    = get_classes('dashboard.catalogue.tables',
                  ('ProductTable', 'CategoryTable'))


class BauerListView(SingleTableView):
    pass


class FinishedListView(SingleTableView):
    pass


class InstructionListView(SingleTableView):
    pass


class UnfinishedListView(SingleTableView):
    template_name = 'dashboard/catalogue/product_list.html'
    table_class = ProductTable
    context_table_name = 'products'

