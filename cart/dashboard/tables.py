from django_tables2 import TemplateColumn
from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_class

ProductTable = get_class('dashboard.catalogue.tables', 'ProductTable')

class UnfinishedTable(ProductTable):
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/catalogue/unfinished_row_actions.html',
        orderable=False)

