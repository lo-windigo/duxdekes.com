import logging
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.template import loader
from oscar.core.loading import get_classes


logger = logging.getLogger('duxdekes.receivers')
order_placed, order_status_changed = get_classes('order.signals',
        ('order_placed', 'order_status_changed'))


@receiver(order_placed)
def notify_jeff(sender, **kwargs):
    try:
        order = kwargs.get('order')
    except:
        logger.warning('Order not sent into notify_jeff() receiver')
        return
    
    send_new_order_notification(order)


@receiver(order_status_changed)
def receive_order_status_change(sender, **kwargs):
    """
    Send any extra notifications based on order status notifications
    """
    try:
        order = kwargs.get('order')
        order_status = kwargs.get('new_status')
    except:
        logger.warning('Missing arguments in receive_order_status_change()')
        return

    # Send notifications based on the new order status
    if order_status == 'Processed':
        send_finalized_order_notification(order)


def send_finalized_order_notification(order):
    """
    Notify a customer once an order has been finalized
    """
    order_context = {
            'order': order,
            }
    email_template = loader.get_template('duxdekes/email/order_finalized.txt')
    email_body = email_template.render(order_context)

    try:
        send_mail('Order #{} Processed'.format(order.number),
                email_body,
                settings.OSCAR_FROM_EMAIL,
                [order.email])
    except Exception as e:
        msg = 'Unable to send new order notification. Error: {}'.format(str(e))
        logger.warning(msg)


def send_new_order_notification(order):
    """
    Send a notification to Jeff about a new order
    TODO: Can be generalized to pull emails from stock record owners
    """

    # Assemble the order details that need to be included in the email
    order_dashboard_url = 'https://{}{}'.format(
            settings.DOMAIN,
            reverse('dashboard:order-detail', kwargs={'number': order.number}))
    order_context = {
            'order': order,
            'order_url': order_dashboard_url,
            }
    email_template = loader.get_template('duxdekes/email/order_placed.txt')
    email_body = email_template.render(order_context)

    # Send email, with all the compiled information
    try:
        send_mail('New Order: #{}'.format(order.number),
                email_body,
                settings.CONTACT_SENDER,
                settings.CONTACT_RECIPIENTS)
    except Exception as e:
        msg = 'Unable to send new order notification. Error: {}'.format(str(e))
        logger.warning(msg)

