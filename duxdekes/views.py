from .util.contact import ContactForm
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from .util.homepage import homepage_data


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


    return render(request,
        'duxdekes/page-home.html',
        {
            'unfinished': unfinished,
            'finished': finished,
            'instructions': instructions,
        })

