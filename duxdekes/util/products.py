
from oscar.core.loading import get_classes, get_model


# Get Oscar classes
ProductClass = get_model('catalogue', 'ProductClass')
Product = get_model('catalogue', 'Product')
Partner = get_model('partner', 'Partner')
StockRecord = get_model('partner', 'StockRecord')

PARTNER=Partner.objects.get(name='Dux Dekes')
UNFINISHED_CLASS=ProductClass.objects.get(name='Unfinished Blanks')


def add_unfinished(**kwargs):
    """
    Add an Unfinished Blank product, and all of the child products

    Args:
    - title: Name/Description of the product
    - pine_price, pine_sku: price and SKU of a pine decoy
    - tupelo_price, tupelo_sku: price and SKU of a tupelo decoy
    - feet_price: Price of optional feet
    """

    product = Product()
    product.title = kwargs['title']
    product.structure = Product.PARENT
    product.product_class = UNFINISHED_CLASS
    product.save()

    # Set up the data to create child products with
    data = {'parent': product}
    data.update(kwargs)

    # If there are pine or Tupelo values, add them as sub-products
    if data['pine_sku'] and data['pine_price']:
        add_pine(**data)

    if data['tupelo_sku'] and data['tupelo_price']:
        add_tupelo(**data)

    return product


def add_unfinished_material(**kwargs):

    variant = Product()
    variant.title = '{} - {}'.format(kwargs['name'], kwargs['parent'].title)
    variant.structure = Product.CHILD
    variant.parent = kwargs['parent']
    variant.save()

    stock = StockRecord()
    stock.product = variant
    stock.partner = PARTNER
    stock.partner_sku = kwargs['sku'] 
    stock.price_excl_tax = kwargs['price']
    stock.save()


def add_pine(**kwargs):
    add_unfinished_material(name='Pine',
            parent=kwargs['parent'],
            sku=kwargs['pine_sku'],
            price=kwargs['pine_price'])


def add_tupelo(**kwargs):
    add_unfinished_material(name='Tupelo',
            parent=kwargs['parent'],
            sku=kwargs['tupelo_sku'],
            price=kwargs['tupelo_price'])

