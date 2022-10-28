from django.views.generic import TemplateView
from oscar.core.loading import get_model


# Dynamically get oscar models
Category = get_model('catalogue', 'Category')
Product = get_model('catalogue', 'Product')


class Contact(TemplateView):
    template_name='page-contact.html'


class HomeView(TemplateView):
    """
    The homepage: list the major product types, along with the categories, and a
    selection of the newest products.
    """
    context_object_name = 'categories'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """
        Provide the complicated context data we need for the homepage
        """

        context = super().get_context_data(**kwargs)
        categories = []
        
        for parent in Category.get_root_nodes():

            related_categories = parent.get_descendants_and_self()

            # Get the newest products from each category tree
            products = Product.browsable.filter(
                    categories__in=related_categories
                    ).order_by('-date_updated')[:3]

            categories.append({
                'category': parent,
                'sub_categories': parent.get_children(),
                'products': products,
                })

        context[self.context_object_name] = categories 
        return context

