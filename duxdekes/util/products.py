from django.core.exceptions import DoesNotExist, MultipleObjectsReturned
from oscar.core.loading import get_classes, get_model


# Get Oscar classes
ProductClass = get_model('catalogue', 'ProductClass')
Product = get_model('catalogue', 'Product')
Partner = get_model('partner', 'Partner')
StockRecord = get_model('partner', 'StockRecord')

PARTNER=Partner.objects.get(name='Dux Dekes')
UNFINISHED_CLASS=ProductClass.objects.get(name='Unfinished Blanks')


def get_pine(unfinished_blank):
    return get_material(unfinished_blank, 'Pine')


def get_material(unfinished_blank, material):

    variants = unfinished_blank.children.all()

    # Load material values based on child products
    for variant in variants:
        if variant.title and variant.title[:4] == material[:4]:
            record = StockRecord.objects.get(product=variant)
            return record

    # Default: material not present, return a bunch of none
    return None


def get_tupelo(unfinished_blank):
    return get_material(unfinished_blank, 'Tupelo')


def save_unfinished(**kwargs):
    """
    Add an Unfinished Blank product, and all of the child products

    Supported Args:
    - title: Name/Description of the product
    - pine_price, pine_sku: price and SKU of a pine decoy
    - tupelo_price, tupelo_sku: price and SKU of a tupelo decoy
    - feet_price: Price of optional feet
    - ...
    """

    updating = 'instance' in kwargs

    if updating:
        product = kwargs['instance']
    else:
        product = Product()
        product.structure = Product.PARENT
        product.product_class = UNFINISHED_CLASS

    product.title = kwargs['title']
    product.save()

    # Set up the data to create child products with
    data = {'parent': product}
    data.update(kwargs)

    # If there are pine or Tupelo values, add them as sub-products
    if data['pine_sku'] and data['pine_price']:
        save_pine(product, **data)
    elif updating:
        remove_pine(product)

    if data['tupelo_sku'] and data['tupelo_price']:
        save_tupelo(product, **data)
    elif updating:
        remove_tupelo(product)

    return product


def save_unfinished_material(product, **kwargs):

    try:
        product.children.get(partner_sku=kwargs['sku'])
        stock = StockRecord()
    except DoesNotExist, MultipleObjectsReturned as e:
        variant = Product()
        variant.structure = Product.CHILD
        variant.title = '{} - {}'.format(kwargs['name'], kwargs['parent'].title)
        variant.parent = product
        variant.save()

        stock = StockRecord()
        stock.product = variant
        stock.partner = PARTNER

    stock.partner_sku = kwargs['sku'] 
    stock.price_excl_tax = kwargs['price']
    stock.save()


def save_pine(product, **kwargs):
    save_unfinished_material(product,
            name='Pine',
            sku=kwargs['pine_sku'],
            price=kwargs['pine_price'])


def save_tupelo(product, **kwargs):
    save_unfinished_material(product,
            name='Tupelo',
            sku=kwargs['tupelo_sku'],
            price=kwargs['tupelo_price'])

