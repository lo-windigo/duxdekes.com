from django_tables2 import A, TemplateColumn
from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
ProductTable = get_class('dashboard.catalogue.tables', 'ProductTable')

class FinishedTable(ProductTable):
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/catalogue/finished_row_actions.html',
        orderable=False)
    title = TemplateColumn(
        verbose_name=_('Title'),
        template_name='dashboard/catalogue/finished_row_title.html',
        order_by='title', accessor=A('title'))

    # Bring over the meta configurations from the parent view
    class Meta(ProductTable.Meta):
        pass


class InstructionsTable(ProductTable):
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/catalogue/instructions_row_actions.html',
        orderable=False)
    title = TemplateColumn(
        verbose_name=_('Title'),
        template_name='dashboard/catalogue/instructions_row_title.html',
        order_by='title', accessor=A('title'))

    # Bring over the meta configurations from the parent view
    class Meta(ProductTable.Meta):
        pass


class WeightlessTable(DashboardTable):
    """
    A view for correcting weightless products
    """
    title = ProductTable.title
    upc = ProductTable.upc
    image = ProductTable.image
    product_class = ProductTable.product_class
    set_weight = TemplateColumn(
        verbose_name=_('Set Weight'),
        template_name='dashboard/catalogue/weightless_row_set_weight.html',
        orderable=False)

    class Meta(DashboardTable.Meta):
        model = Product
        fields = ('upc', 'date_updated')
        sequence = ('title', 'upc', 'image', 'product_class', 
                    '...', 'date_updated')
        order_by = '-date_updated'


class UnfinishedTable(ProductTable):
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/catalogue/unfinished_row_actions.html',
        orderable=False)
    title = TemplateColumn(
        verbose_name=_('Title'),
        template_name='dashboard/catalogue/unfinished_row_title.html',
        order_by='title', accessor=A('title'))

    # Bring over the meta configurations from the parent view
    class Meta(ProductTable.Meta):
        pass

