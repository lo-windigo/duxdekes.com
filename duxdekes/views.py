from .util.contact import ContactForm
from products.models import Product, ProductCategory
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings


def about(request):
    """
    About Dux Dekes' wood carvings
    """
    return render(request, 'duxdekes/page-about.html')


def about_artist(request):
    """
    About Jeff Duxbury
    """
    return render(request, 'duxdekes/page-about-artist.html')


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


def contact_sent(request):
    """
    Status message: Contact was successfully sent
    """
    return render(request, 'duxdekes/page-contact-sent.html')


def home(request):
    """
    The homepage: list the major product types, along with the categories, and a
    selection of the newest products.
    """

    # Set up the dicts that will be sent in as context
    categories = {}
    new_products = {}

    # Get some QueryManagers for use in retrieving type-related objects
    category_qm = ProductCategory.objects.exclude(hidden=True).order_by('description')
    product_qm = Product.objects.exclude(hidden=True).order_by('-updated')

    for category_type in (ProductCategory.UNFINISHED,
            ProductCategory.FINISHED,
            ProductCategory.INSTRUCTION,
            ProductCategory.MATERIAL):

        type_categories = category_qm.filter(category_type=category_type)
        type_products = product_qm.filter(category__category_type=category_type)

        # Get all categories
        # TODO: This doesn't work.
        categories[category_type] = list(type_categories)

        # Get the latest 4 products from this category type
        # TODO
        new_products[category_type] = type_products[:4]
    
    return render(request,
            'duxdekes/page-home.html',
            {
                'categories': categories,
                'new_products': new_products,
            })

