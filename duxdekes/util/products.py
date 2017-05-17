from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from oscar.core.loading import get_classes, get_model



# Set up some product name constants
PINE = 'Pine'
TUPELO = 'Tupelo'
FEET = 'with Feet'

# Get Oscar classes
ProductClass = get_model('catalogue', 'ProductClass')
Product = get_model('catalogue', 'Product')
Partner = get_model('partner', 'Partner')
StockRecord = get_model('partner', 'StockRecord')



def get_partner():
    try:
        return Partner.objects.get(name='Dux Dekes')
    except Exception:
        return None


def get_unfinished_class():
    try:
        return ProductClass.objects.get(name='Unfinished Blanks')
    except Exception:
        return None


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
    - upc: Stock ID of this product
    - pine_price, pine_upc: price and SKU of a pine decoy
    - tupelo_price, tupelo_upc: price and SKU of a tupelo decoy
    - feet_price: Price of optional feet
    - ...
    """

    updating = 'instance' in kwargs

    if updating:
        product = kwargs['instance']
        old_upc = product.upc
    else:
        product = Product()
        product.structure = Product.PARENT
        product.product_class = get_unfinished_class()

    product.title = kwargs['title']
    product.upc = kwargs['upc']
    product.save()

    # If there are pine or Tupelo values, add them as sub-products
    if kwargs['pine_price']:
        pine_args = kwargs
        pine_args.update({'old_upc': old_upc,})
        save_pine(product, **pine_args)

    elif updating:
        remove_pine(product)

    if kwargs['tupelo_price']:
        tupelo_args = kwargs
        tupelo_args.update({'old_upc': old_upc,})
        save_tupelo(product, **tupelo_args)
    elif updating:
        remove_tupelo(product)

    return product


def save_unfinished_material(product, **kwargs):
    """
    Save a child product that represents a material that this decoy can be made
    out of
    """
    try:
        if not kwargs['old_upc']:
            raise ObjectDoesNotExist()

        stock = StockRecord.objects.filter(
                product__in=product.children.all()).get(
                partner_sku=kwargs['old_upc'])
        variant = stock.product

    except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
        variant = Product()
        variant.structure = Product.CHILD
        variant.parent = product

        stock = StockRecord()
        stock.product = variant
        stock.partner = get_partner()

    variant.title = '{} — {}'.format(kwargs['name'], product.title)
    variant.save()

    stock.partner_sku = kwargs['upc'] 
    stock.price_excl_tax = kwargs['price']
    stock.save()


def save_pine(product, **kwargs):
    """
    A wrapper around save_material that provides the sensible defaults for pine
    """
    upc_format = '{}_P'
    upc = upc_format.format(kwargs['upc'])

    if kwargs['old_upc']:
        old_upc = upc_format.format(kwargs['old_upc'])
    else:
        old_upc = None

    save_unfinished_material(product,
            name=PINE,
            upc=upc,
            old_upc=old_upc,
            price=kwargs['pine_price'])

    if kwargs['feet_price']:
        save_pine_feet(product, **kwargs)


def save_pine_feet(product, **kwargs):
    """
    A wrapper around save_material that provides the sensible defaults for pine
    with optional feet
    """
    name_with_feet = '{} {}'.format(PINE, FEET)
    price_with_feet = int(kwargs['pine_price']) + int(kwargs['feet_price'])
    upc_format = '{}_PF'
    upc = upc_format.format(kwargs['upc'])

    if kwargs['old_upc']:
        old_upc = upc_format.format(kwargs['old_upc'])
    else:
        old_upc = None

    save_unfinished_material(product,
            name=name_with_feet,
            upc=upc,
            old_upc=old_upc,
            price=price_with_feet)


def save_tupelo(product, **kwargs):
    """
    A wrapper around save_material that provides the sensible defaults for
    products offered in tupelo
    """
    upc_format = '{}_T'
    upc = upc_format.format(kwargs['upc'])

    if kwargs['old_upc']:
        old_upc = upc_format.format(kwargs['old_upc'])
    else:
        old_upc = None

    save_unfinished_material(product,
            name=TUPELO,
            upc=upc,
            old_upc=old_upc,
            price=kwargs['tupelo_price'])

    if kwargs['feet_price']:
        save_tupelo_feet(product, **kwargs)


def save_tupelo_feet(product, **kwargs):
    """
    A wrapper around save_material that provides the sensible defaults for
    tupelo, with optional feet
    """
    name_with_feet = '{} {}'.format(TUPELO, FEET)
    price_with_feet = int(kwargs['tupelo_price']) + int(kwargs['feet_price'])
    upc_format = '{}_TF'
    upc = upc_format.format(kwargs['upc'])

    if kwargs['old_upc']:
        old_upc = upc_format.format(kwargs['old_upc'])
    else:
        old_upc = None

    save_unfinished_material(product,
            name=name_with_feet,
            upc=upc,
            old_upc=old_upc,
            price=price_with_feet)


def remove_material(product, description):
    """
    Remove a child product(s) representing an unfinished blank material
    """
    material_options = product.children.filter(title__startswith=material)

    for material in material_options:
        material.delete()


def remove_pine(product):
    remove_material(product, PINE)


def remove_tupelo(product):
    remove_material(product, TUPELO)

