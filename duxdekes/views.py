from .util.contact import ContactForm
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.conf import settings
from oscar.core.loading import get_model
from .util.homepage import homepage_data


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

    # Get all the categories (and subcategories)
    try:
        unfinished = homepage_data('Unfinished Blanks')
    except Exception as e:
        unfinished = {
            'categories': [],
            'products': [],
        }

    try:
        finished = homepage_data('Finished Carvings')
    except:
        finished = {
            'categories': [],
            'products': [],
        }

    try:
        instructions = homepage_data('Instructions')
    except:
        instructions = {
            'categories': [],
            'products': [],
        }


    """
    # Get some QueryManagers for use in retrieving type-related objects
    category_qm = ProductCategory.objects.exclude(hidden=True).order_by('description')
    new_products[ProductCategory.FINISHED] = FinishedCarving.objects.exclude(hidden=True).order_by('-updated')[:4]
    new_products[ProductCategory.INSTRUCTION] = Instructions.objects.exclude(hidden=True).order_by('-updated')[:4]
    new_products[ProductCategory.UNFINISHED] = UnfinishedBlank.objects.exclude(hidden=True).order_by('-updated')[:4]

    for category_type in (ProductCategory.UNFINISHED,
            ProductCategory.FINISHED,
            ProductCategory.INSTRUCTION,
            ProductCategory.MATERIAL):

        type_categories = list(category_qm.filter(category_type=category_type))

        # Get all categories
        categories[category_type] = type_categories
    """ 

    return render(request,
        'duxdekes/page-home.html',
        {
            'unfinished': unfinished,
            'finished': finished,
            'instructions': instructions,
        })

