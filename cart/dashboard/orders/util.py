from oscar.core.loading import get_model

"""
Shipping report data
"""
ORDER_ID = 'Order ID'
NUM_ITEMS = '# of items'
SHIPPING_EST = 'Shipping (est)'
SHIPPING_ACT = 'Shipping (actual)'
AVG_SHIPPING_PER_ITEM = 'Average shipping per item'

CURRENCY_HEADINGS = (SHIPPING_EST, SHIPPING_ACT, AVG_SHIPPING_PER_ITEM)
REPORT_HEADINGS = (ORDER_ID, NUM_ITEMS) + CURRENCY_HEADINGS

Order = get_model('order', 'Order')


def get_orders(date_range=False):
    """
    Get orders for the report
    :param date_range:
    :return:
    """
    if date_range:
        return Order.objects.filter('order_date')

    return Order.objects.all()


def get_order_statistics(order):
    """
    Get a statistics dictionary from an order object
    :type order: Order
    :return: dict
    """
    avg_shipping_per_item = order.final_shipping / order.num_items

    return {
        ORDER_ID: order.number,
        NUM_ITEMS: order.num_items,
        SHIPPING_EST: order.shipping_incl_tax,
        SHIPPING_ACT: order.final_shipping,
        AVG_SHIPPING_PER_ITEM: avg_shipping_per_item
    }
