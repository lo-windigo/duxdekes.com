from .util.contact import ContactForm
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import ListView, TemplateView
from oscar.core.loading import get_model


# Dynamically get oscar models
Category = get_model('catalogue', 'Category')
Product = get_model('catalogue', 'Product')


def contact(request):
    """
    Send Jeff a message
    """

    # Handle any form submissions
    if request.method == 'POST':
        form = ContactForm(request.POST)

        # Send message if no problems were detected
        if form.is_valid():

            message_template= """
            Name: {name}
            Email: {email}
            Message:
            {msg}
            """

            message_body = message_template.format(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    msg=form.cleaned_data['message'])

            send_mail(settings.CONTACT_SUBJECT,
                    message_body,
                    settings.CONTACT_SENDER,
                    settings.CONTACT_RECIPIENTS)

            return redirect('contact_sent')

    # If no submission has occurred, start a blank form
    else:
        form = ContactForm()

    return render(request, 'duxdekes/page-contact.html', {'form': form})


class ContactSent(TemplateView):
    template_name='duxdekes/page-contact-sent.html'


class HomeView(TemplateView):
    """
    The homepage: list the major product types, along with the categories, and a
    selection of the newest products.
    """
    context_object_name = 'categories'
    #queryset = Category.get_root_nodes()
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
            products = Product.objects.filter(
                    categories__in=related_categories
                    ).order_by('-date_updated')[:3]

            categories.append({
                'category': parent,
                'sub_categories': parent.get_children(),
                'products': products,
                })

        context[self.context_object_name] = categories 
        return context

