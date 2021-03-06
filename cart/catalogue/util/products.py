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
INSTRUCTIONS_WITH_BLANK_UPC = '{}B'

# Get Oscar classes
#InstructionsWithBlankProduct = get_model('catalogue', 'InstructionsWithBlankProduct')



def get_partner():
    """
    Get the only partner that matters to Dux Dekes
    """
    Partner = get_model('partner', 'Partner')

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
    ProductClass = get_model('catalogue', 'ProductClass')

    klass, created = ProductClass.objects.get_or_create(name=name,
            defaults={
                'requires_shipping': True,
                'track_stock': False,
                })

    #if created:
    #    print('Product class {} was created for the first time'.format(name))

    return klass


def get_material(unfinished_blank, upc_format, original_upc = None):
    """
    Get a stock record for a unfinished blank material option
    """
    StockRecord = get_model('partner', 'StockRecord')

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


def get_instructions_alone(instructions, original_upc = None):
    variant, _ = get_instructions_variants(instructions)
    return variant


def get_instructions_with_blank(instructions, original_upc = None):
    _, variant = get_instructions_variants(instructions)
    return variant


#def get_instructions_variants(instructions):
#    """
#    Get the variants for an instructions product
#    """
#    instructions_alone = None
#    instructions_with_blank = None
#
#    for variant in instructions.children.all():
#        if isinstance(variant, InstructionsWithBlankProduct):
#            instructions_with_blank = variant
#        else:
#            instructions_alone = variant
#
#    return instructions_alone, instructions_with_blank


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
    - box: The box size to be associated with this blank
    - weight: The weight of a single blank
    - instance: The object to update
    """

    Product = get_model('catalogue', 'Product')
    StockRecord = get_model('partner', 'StockRecord')

    if 'instance' in kwargs:
        product = kwargs['instance']
    else:
        product = Product()
        product.product_class = get_finished_class()

    product.title = kwargs['title']
    product.upc = kwargs['upc']
    product.attr.box = kwargs['attr_box'] 
    product.attr.weight = kwargs['attr_weight'] 
    product.save()

    # Set stock record AFTER the object's been saved
    stock,_ = StockRecord.objects.get_or_create(product=product,
            defaults={
                'partner': get_partner() 
                })

    stock.product = product
    stock.partner_sku = kwargs['upc']
    stock.price_excl_tax = kwargs['price']
    stock.save()

    return product


#def save_instructions(**kwargs):
#    """
#    Add or update Instructions product
#
#    Supported Args:
#    - title: Name/Description of the product
#    - upc: Stock ID of this product
#    - original_upc: Stock ID of this product (prior to editing)
#    - price: price of instructions
#    - blank: the connected unfinished blank
#    - price_with_blank: price of the instructions with the matching unfinished
#      blank
#    - instance: The object to update
#    """
#    updating = 'instance' in kwargs
#
#    if updating:
#        instructions = kwargs['instance']
#    else:
#        instructions = Product()
#        instructions.product_class = get_instructions_class()
#        instructions.structure = Product.PARENT
#
#    instructions.title = kwargs['title']
#    # NO UPC. Parents can't have stock records, and products can't share UPCs.
#    # So NO UPC FOR YOU, parent product.
#    instructions.upc = None
#    instructions.save()
#
#    # Store the associated blank and price as a child product
#    if 'blank' in kwargs and 'price_with_blank' in kwargs and \
#             kwargs['blank'] and kwargs['price_with_blank']:
#        save_instructions_with_blank(instructions,
#                Product.objects.get(pk=kwargs['blank']),
#                kwargs['price_with_blank'],
#                kwargs['upc'])
#
#    # Remove the matching blank if the fields were erased
##    elif updating:
##       pass
#        #for matching_blank in product.children:
#        #    matching_blank.delete()
#
#    # Add a product for the instructions, without a blank
#    save_instructions_alone(instructions,
#            kwargs['price'],
#            kwargs['upc'])
#
#    return instructions
#
#
#def save_instructions_alone(instructions, price, upc, old_upc=None):
#    """
#    Add or update Instructions child product
#
#    Supported Args:
#    - instructions: product object that this should be a child of
#    - price: price of instructions
#    - upc: product UPC or SKU
#    - old_upc: original stock ID of this product (optional)
#    """
#    variant = None
#
#    # Try to get the stock record with the old SKU first
#    try:
#        variant = Product.objects.get(upc=old_upc)
#    except:
#        pass
#
#    if not variant:
#        try:
#            variant = Product.objects.get(upc=upc)
#
#        except:
#            variant = Product()
#            variant.parent = instructions
#            variant.structure = Product.CHILD
#
#    variant.upc = upc
#    variant.title = INSTRUCTIONS_ALONE.format(instructions.title)
#    variant.save()
#
#    save_instructions_variant_stock(variant, price)
#
#
#def save_instructions_with_blank(instructions, blank, price, upc, old_upc=None):
#    """
#    Add or update Instructions child product
#
#    Supported Args:
#    - instructions: product object that this should be a child of
#    - blank: the connected unfinished blank (optional)
#    - price: price of instructions
#    - upc: product UPC or SKU of the parent item
#    - old_upc: original stock ID of this product (optional)
#    """
#    variant = None
#    upc_with_blank = INSTRUCTIONS_WITH_BLANK_UPC.format(upc)
#
#    # Try to get the stock record with the old SKU first
#    try:
#        variant = InstructionsWithBlankProduct.objects.filter(
#                parent=instructions
#                ).get(upc=INSTRUCTIONS_WITH_BLANK_UPC.format(old_upc))
#        variant.upc = upc_with_blank 
#    except:
#        pass
#
#    if not variant:
#        variant, created = InstructionsWithBlankProduct.objects.get_or_create(
#                upc=upc_with_blank)
#
#        if created:
#            variant.parent = instructions
#            variant.structure = Product.CHILD
#
#    variant.title = INSTRUCTIONS_WITH_BLANK.format(kwargs['title'], blank.title),
#    variant.blank = blank
#
#    variant.save()
#
#    save_instructions_variant_stock(variant, price)
#
#
#def save_instructions_variant_stock(variant, price):
#    """
#    Create or update a stock record for an instructions variant
#
#    Supported Args:
#    - variant: a child product that represents an Instructions variant
#    - price: price of instructions
#    - old_upc: original stock ID of this product (optional)
#    """
#    try:
#        stock = StockRecord.objects.get(product=variant)
#    except:
#        stock = StockRecord()
#        stock.product = variant
#        stock.partner = get_partner()
#
#    stock.price_excl_tax = price
#    stock.partner_sku = variant.upc
#
#    stock.save()


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

    Product = get_model('catalogue', 'Product')
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
    product.attr.box = kwargs['attr_box'] 
    product.attr.weight = kwargs['attr_weight'] 
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
    Product = get_model('catalogue', 'Product')
    StockRecord = get_model('partner', 'StockRecord')

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

    try:
        variant.attr.box = kwargs['attr_box'] 
    except:
        pass

    try:
        variant.attr.weight = kwargs['attr_weight'] 
    except:
        pass

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
    material_args['attr_box'] = kwargs.get('attr_box', None)
    material_args['attr_weight'] = kwargs.get('attr_weight', None)
    
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
    material_args['attr_box'] = kwargs.get('attr_box', None)
    material_args['attr_weight'] = kwargs.get('attr_weight', None)
    
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
    material_args['attr_box'] = kwargs.get('attr_box', None)
    material_args['attr_weight'] = kwargs.get('attr_weight', None)
    
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
    material_args['attr_box'] = kwargs.get('attr_box', None)
    material_args['attr_weight'] = kwargs.get('attr_weight', None)
    
    if 'original_upc' in kwargs:
        material_args['original_upc'] = kwargs['original_upc']

    save_unfinished_material(product, **material_args)


def remove_material(product, upc_format, **kwargs):
    """
    Remove a child product(s) representing an unfinished blank material
    """
    StockRecord = get_model('partner', 'StockRecord')

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

