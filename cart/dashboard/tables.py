from django_tables2 import A, TemplateColumn
from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_class

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

