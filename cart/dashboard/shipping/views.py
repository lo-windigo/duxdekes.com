from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django_tables2 import SingleTableView
from oscar.core.loading import get_class, get_classes, get_model
from . import tables

Box = get_model('shipping', 'Box')

BOX_TEMPLATE_DIR = 'dashboard/shipping'


class BoxListView(SingleTableView):
    template_name = '{}/list.html'.format(BOX_TEMPLATE_DIR)
    table_class = tables.BoxTable
    context_table_name = 'boxes'
    model = Box

    def get_table(self, **kwargs):
        """
        Set the table caption by overriding the parent method
        """
        table = super().get_table(**kwargs)
        table.caption = 'Box Sizes'
        return table

class BoxMixin():
    fields = ['length', 'width', 'height']
    model = Box
    success_url = reverse_lazy('dashboard:shipping:box-list')

class BoxCreateView(BoxMixin, generic.CreateView):
    template_name = '{}/update.html'.format(BOX_TEMPLATE_DIR)


class BoxUpdateView(BoxMixin, generic.UpdateView):
    template_name = '{}/update.html'.format(BOX_TEMPLATE_DIR)


class BoxDeleteView(BoxMixin, generic.DeleteView):
    template_name = '{}/delete.html'.format(BOX_TEMPLATE_DIR)

