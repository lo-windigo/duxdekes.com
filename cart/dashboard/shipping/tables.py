from django_tables2 import A, TemplateColumn
from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')


class BoxTable(DashboardTable):
    dimensions = TemplateColumn(
        verbose_name=_('Dimensions'),
        template_name='dashboard/shipping/row_dimension.html',
        order_by='length')
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/shipping/row_actions.html',
        orderable=False)

    # Bring over the meta configurations from the parent view
    class Meta(DashboardTable.Meta):
        pass

    def render_dimensions(self, record):
        """
        Get a string representation of the box
        """
        return str(record)

