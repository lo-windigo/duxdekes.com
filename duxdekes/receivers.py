from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.template import loader
from oscar.core.loading import get_class


order_placed = get_class('order.signals', 'order_placed')


@reciever(order_placed)
def notify_jeff(sender, **kwargs):

    if 'order' not in kwargs:
        return
    
    # Assemble the order details that need to be included in the email
    order = kwargs['order']
    order_context = {
            'order': order,
            'order_url': reverse('dashboard:order-detail', order.number),
            }
    email_template = loader.get_template('duxdekes/email/order_placed.txt')
    email_body = email_template.render(order_context)

    # Send email, with all the compiled information
    send_mail('New Order: #{}'.format(order.number),
            email_body,
            settings.CONTACT_SENDER,
            settings.CONTACT_RECIPIENTS)

