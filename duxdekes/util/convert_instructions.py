from oscar.core.loading import get_model
from duxdekes.util import products

InstructionsProduct = get_model('catalogue', 'InstructionsProduct')
Product = get_model('catalogue', 'Product')


def convert_instructions():
    """
    Convert instructions imported as basic products into the
    InstructionsProduct model
    """
    instructions_with_blank = []
    instructions_class = products.get_instructions_class()
    instructions = Product.objects.filter(product_class=instructions_class,
            structure=Product.PARENT)

    # Run through all of the old-style instructions and save them as new
    # instructions
    for old_instructions in instructions.all():
        if isinstance(old_instructions, InstructionsProduct):
            continue

        if old_instructions.upc and old_instructions.upc.upper()[-1] == 'B':
            instructions_with_blank.append(old_instructions)
            continue

        new_instructions = InstructionsProduct()
        new_instructions.title = old_instructions.title 
        new_instructions.sku = old_instructions.upc.upper()

        price_child = old_instructions.children.get()
        price_stock = price_child.stockrecords.get()

        new_instructions.price = price_stock.price_excl_tax
        new_instructions.save()
    
    # Get the "instructions with blank" prices
    for old_instructions in instructions_with_blank:
        try:
            match = InstructionsProduct.objects.get(sku=old_instructions.upc.upper()[:-1])
        except Exception as e:
            print(e)
            continue

        price_child = old_instructions.children.get()
        price_stock = price_child.stockrecords.get()

        match.price_with_blank = price_stock.price_excl_tax
        match.save()

