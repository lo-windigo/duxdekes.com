from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from oscar.core.loading import get_classes, get_model



# Set up some product name constants
PINE = 'Pine'
PINE_UPC = '{}_P'
PINE_FEET_UPC = '{}_PF'
TUPELO = 'Tupelo'
TUPELO_UPC = '{}_T'
TUPELO_FEET_UPC = '{}_TF'
FEET = 'with Feet'
INSTRUCTIONS_ALONE = '{} Painting Kit'
INSTRUCTIONS_WITH_BLANK = '{} Painting Kit & {} blank'

# Get Oscar classes
InstructionsWithBlankProduct = get_model('catalogue', 'InstructionsWithBlankProduct')
ProductClass = get_model('catalogue', 'ProductClass')
Product = get_model('catalogue', 'Product')
Partner = get_model('partner', 'Partner')
StockRecord = get_model('partner', 'StockRecord')



def get_partner():
    partner, created = Partner.objects.get_or_create(name='Dux Dekes')

    #if created:
    #    print('Partner was created for the first time')

    return partner


def get_finished_class():
    return get_product_class('Finished Decoys')


def get_instructions_class():
    return get_product_class('Instructions')


def get_book_class():
    return get_product_class('Instruction Books')


def get_unfinished_class():
    return get_product_class('Unfinished Blanks')


def get_product_class(name):
    """
    Fetch a generic product class, or create it if this is the first time called
    """
    klass, created = ProductClass.objects.get_or_create(name=name,
            defaults={
                'requires_shipping': True,
                'track_stock': False,
                })

    #if created:
    #    print('Product class {} was created for the first time'.format(name))

    return klass


def get_material(unfinished_blank, upc_format, original_upc = None):

    if original_upc:
        upc = upc_format.format(original_upc)
    else:
        upc = upc_format.format(unfinished_blank.upc)

    try:
        return StockRecord.objects.filter(
                product__in=unfinished_blank.children.all()).get(
                partner_sku=upc)

    # Default: material not present, return a bunch of none
    except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
        return None


def get_pine(unfinished_blank, original_upc = None):
    return get_material(unfinished_blank, PINE_UPC, original_upc)


def get_pine_feet(unfinished_blank, original_upc = None):
    return get_material(unfinished_blank, PINE_FEET_UPC, original_upc)


def get_tupelo(unfinished_blank, original_upc = None):
    return get_material(unfinished_blank, TUPELO_UPC, original_upc)


def get_tupelo_feet(unfinished_blank, original_upc = None):
    return get_material(unfinished_blank, TUPELO_FEET_UPC, original_upc)


def save_finished(**kwargs):
    """
    Add a Finished Decoy product

    Supported Args:
    - title: Name/Description of the product
    - upc: Stock ID of this product
    - original_upc: Stock ID of this product (prior to editing)
    - price: price of a decoy
    - instance: The object to update
    """

    updating = 'instance' in kwargs

    if updating:
        product = kwargs['instance']
        stock, created = StockRecord.objects.get(product=product)

        if created:
            stock.partner = get_partner()
    else:
        product = Product()
        product.product_class = get_finished_class()

    product.title = kwargs['title']
    product.upc = kwargs['upc']
    product.save()

    # Set stock record AFTER the object's been saved
    stock.product = product
    stock.partner_sku = kwargs['upc']
    stock.price_excl_tax = kwargs['price']
    stock.save()

    return product


def save_instructions(**kwargs):
    """
    Add or update Instructions product

    Supported Args:
    - title: Name/Description of the product
    - upc: Stock ID of this product
    - original_upc: Stock ID of this product (prior to editing)
    - price: price of instructions
    - blank: the connected unfinished blank
    - price_with_blank: price of the instructions with the matching unfinished
      blank
    - instance: The object to update
    """

    updating = 'instance' in kwargs
    instructions_class = get_instructions_class()

    if updating:
        product = kwargs['instance']
    else:
        product = Product()
        product.product_class = instructions_class
        product.structure = Product.PARENT

    product.title = kwargs['title']
    product.upc = kwargs['upc']
    product.save()

    old_upc = None
    if 'original_upc' in kwargs:
        old_upc = kwargs['original_upc']

    # Store the associated blank and price as a child product
    if 'blank' in kwargs and 'price_with_blank' in kwargs:
        blank = Product.objects.get(pk=kwargs['blank'])

        save_instructions_child(product,
                INSTRUCTIONS_WITH_BLANK.format(kwargs['title'], blank.title),
                kwargs['price_with_blank'],
                old_upc,
                blank)

    # Remove the matching blank if the fields were erased
    elif updating:
        pass
        #for matching_blank in product.children:
        #    matching_blank.delete()

    # Add a product for the instructions, without a blank
    save_instructions_child(product,
            INSTRUCTIONS_ALONE.format(kwargs['title']),
            kwargs['price'],
            old_upc)

    return product


def save_instructions_child(instructions, title, price, old_upc=None, blank=None):
    """
    Add or update Instructions child product

    Supported Args:
    - instructions: product object that this should be a child of
    - price: price of instructions
    - upc: Stock ID of this product
    - original_upc: original stock ID of this product (optional)
    - blank: the connected unfinished blank (optional)
    """
    variants = StockRecord.objects.filter(product__in=instructions.children.all())
    stock = None
    variant = None

    # Try to get the stock record with the old SKU first
    if old_upc:
        try:
            stock = variants.get(sku=old_upc)
            stock.sku = instructions.upc
            variant = stock.product

    # Create/fetch the stock record if it hasn't been found yet
    if not stock:
        stock, created = variants.get_or_create(sku=instructions.upc)

        if created:
            if blank:
                variant = InstructionsWithBlankProduct()
            else:
                variant = Product()

            variant.parent = instructions
            variant.product_class = instructions_class
            variant.structure = Product.CHILD
            variant.save()

            stock.partner = get_partner()
            stock.product = variant
        else:
            variant = stock.product

    # Update all of the relevant details for this variant
    stock.price_excl_tax = price
    stock.sku = instructions.upc
    stock.save()
    
    if blank:
        variant.blank = blank
        variant.save()


def save_unfinished(**kwargs):
    """
    Add an Unfinished Blank product, and all of the child products

    Supported Args:
    - title: Name/Description of the product
    - upc: Stock ID of this product
    - original_upc: Stock ID of this product (prior to editing)
    - pine_price, pine_upc: price and SKU of a pine decoy
    - tupelo_price, tupelo_upc: price and SKU of a tupelo decoy
    - feet_price: Price of optional feet
    - instance: The object to update
    """

    updating = 'instance' in kwargs
    material_args = dict(kwargs)

    if updating:
        product = kwargs['instance']
        material_args.update({'original_upc': product.upc,})
    else:
        product = Product()
        product.structure = Product.PARENT
        product.product_class = get_unfinished_class()

    product.title = kwargs['title']
    product.upc = kwargs['upc']
    product.save()

    # If there are pine or Tupelo values, add them as sub-products
    if kwargs['pine_price']:
        save_pine(product, **material_args)
        if kwargs['feet_price']:
            save_pine_feet(product, **material_args)
    elif updating:
        remove_pine(product, **material_args)
        remove_pine_feet(product, **material_args)

    if kwargs['tupelo_price']:
        save_tupelo(product, **material_args)
        if kwargs['feet_price']:
            save_tupelo_feet(product, **material_args)
    elif updating:
        remove_tupelo(product, **material_args)
        remove_tupelo_feet(product, **material_args)

    if not kwargs['feet_price']:
        remove_pine_feet(product, **material_args)
        remove_tupelo_feet(product, **material_args)

    return product


def save_unfinished_material(product, **kwargs):
    """
    Save a child product that represents a material that this decoy can be made
    out of
    """
    upc_format = kwargs['upc_format']
    upc = upc_format.format(product.upc)

    if 'original_upc' in kwargs:
        stock = get_material(product, upc_format, kwargs['original_upc'])

    if stock:
        variant = stock.product
    else:
        variant = Product()
        variant.structure = Product.CHILD
        variant.parent = product

        stock = StockRecord()
        stock.partner = get_partner()

    variant.title = '{} — {}'.format(kwargs['name'], product.title)
    variant.save()

    # Set variant AFTER the object's been saved
    stock.product = variant
    stock.partner_sku = upc 
    stock.price_excl_tax = kwargs['price']

    stock.save()


def save_pine(product, **kwargs):
    """
    A wrapper around save_material that provides the sensible defaults for pine
    """
    material_args = dict()

    material_args['name'] = PINE
    material_args['upc_format'] = PINE_UPC
    material_args['price'] = kwargs['pine_price']
    
    if 'original_upc' in kwargs:
        material_args['original_upc'] = kwargs['original_upc']

    save_unfinished_material(product, **material_args)


def save_pine_feet(product, **kwargs):
    """
    A wrapper around save_material that provides the sensible defaults for pine
    with optional feet
    """
    material_args = dict()

    material_args['name'] = '{} {}'.format(PINE, FEET)
    material_args['upc_format'] = PINE_FEET_UPC
    material_args['price'] = int(kwargs['pine_price']) + int(kwargs['feet_price'])
    
    if 'original_upc' in kwargs:
        material_args['original_upc'] = kwargs['original_upc']

    save_unfinished_material(product, **material_args)


def save_tupelo(product, **kwargs):
    """
    A wrapper around save_material that provides the sensible defaults for
    products offered in tupelo
    """
    material_args = dict()

    material_args['name'] = TUPELO
    material_args['upc_format'] = TUPELO_UPC
    material_args['price'] = kwargs['tupelo_price']
    
    if 'original_upc' in kwargs:
        material_args['original_upc'] = kwargs['original_upc']


    save_unfinished_material(product, **material_args)


def save_tupelo_feet(product, **kwargs):
    """
    A wrapper around save_material that provides the sensible defaults for
    tupelo, with optional feet
    """
    material_args = dict()

    material_args['name'] = '{} {}'.format(TUPELO, FEET)
    material_args['upc_format'] = TUPELO_FEET_UPC
    material_args['price'] = int(kwargs['tupelo_price']) + int(kwargs['feet_price'])
    
    if 'original_upc' in kwargs:
        material_args['original_upc'] = kwargs['original_upc']

    save_unfinished_material(product, **material_args)


def remove_material(product, upc_format, **kwargs):
    """
    Remove a child product(s) representing an unfinished blank material
    """
    if 'original_sku' in kwargs:
        upc = upc_format.format(kwargs['original_sku'])
    else:
        upc = upc_format.format(kwargs['upc'])

    try:
        stock = StockRecord.objects.get(partner_sku=upc)
        material = stock.product
        material.delete()
    except Exception as e:
        debug = """
        Tried to delete {}, which failed; possibly no big deal.
        """
        print(debug.format(upc))


def remove_pine(product, **kwargs):
    remove_material(product, PINE_UPC, **kwargs)


def remove_pine_feet(product, **kwargs):
    remove_material(product, PINE_FEET_UPC, **kwargs)


def remove_tupelo(product, **kwargs):
    remove_material(product, TUPELO_UPC, **kwargs)


def remove_tupelo_feet(product, **kwargs):
    remove_material(product, TUPELO_FEET_UPC, **kwargs)

