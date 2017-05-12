from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from oscar.core.loading import get_classes, get_model


# Set up some product name constants
PINE = 'Pine'
TUPELO = 'Tupelo'

# Get Oscar classes
ProductClass = get_model('catalogue', 'ProductClass')
Product = get_model('catalogue', 'Product')
Partner = get_model('partner', 'Partner')
StockRecord = get_model('partner', 'StockRecord')

# Get the prerequisite related objects
PARTNER=Partner.objects.get(name='Dux Dekes')
UNFINISHED_CLASS=ProductClass.objects.get(name='Unfinished Blanks')


def get_pine(unfinished_blank):
    return get_material(unfinished_blank, 'Pine')


def get_material(unfinished_blank, material):

    try:
        variants = unfinished_blank.children.all()

        # Load material values from child products
        for variant in variants:
            if variant.title and variant.title[:4] == material[:4]:
                record = StockRecord.objects.get(product=variant)
                return record

    except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
        pass

    # Default: material not present, return a bunch of none
    return None


def get_tupelo(unfinished_blank):
    return get_material(unfinished_blank, TUPELO)


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

    # If there are pine or Tupelo values, add them as sub-products
    if kwargs['pine_sku'] and kwargs['pine_price']:
        save_pine(product, **kwargs)
    elif updating:
        remove_pine(product)

    if kwargs['tupelo_sku'] and kwargs['tupelo_price']:
        save_tupelo(product, **kwargs)
    elif updating:
        remove_tupelo(product)

    return product


def save_unfinished_material(product, **kwargs):
    """
    xxx
    """
    try:
        variant = product.children.get(title__startswith=kwargs['name'])
        stock = StockRecord.objects.get(product=variant)

    except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
        variant = Product()
        variant.structure = Product.CHILD
        variant.title = '{} - {}'.format(kwargs['name'], product.title)
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
            name=PINE,
            sku=kwargs['pine_sku'],
            price=kwargs['pine_price'])


def save_tupelo(product, **kwargs):
    save_unfinished_material(product,
            name=TUPELO,
            sku=kwargs['tupelo_sku'],
            price=kwargs['tupelo_price'])


def remove_material(product, sku, description):
    """
    Remove a child product representing an unfinished blank material
    TODO
    """
    pass


def remove_pine(product, sku):
    remove_material(product, sku, PINE)


def remove_tupelo(product, sku):
    remove_material(product, sku, TUPELO)

