from cart.catalogue.util import products


"""
This has moved - include redirect functions to avoid having to go back and
change everything!
"""
def get_partner():
    return products.get_partner()

def get_finished_class():
    return products.get_finished_class()

def get_instructions_class():
    return products.get_instructions_class()

def get_book_class():
    return products.get_book_class()

def get_unfinished_class():
    return products.get_unfinished_class()

def get_material(unfinished_blank, upc_format, original_upc = None):
    return products.get_material(unfinished_blank, upc_format, original_upc = None)

def get_instructions_alone(instructions, original_upc = None):
    return products.get_instructions_alone(instructions, original_upc = None)

def get_instructions_with_blank(instructions, original_upc = None):
    return products.get_instructions_with_blank(instructions, original_upc = None)

def get_pine(unfinished_blank, original_upc = None):
    return products.get_pine(unfinished_blank, original_upc = None)

def get_pine_feet(unfinished_blank, original_upc = None):
    return products.get_pine_feet(unfinished_blank, original_upc = None)

def get_tupelo(unfinished_blank, original_upc = None):
    return products.get_tupelo(unfinished_blank, original_upc = None)

def get_tupelo_feet(unfinished_blank, original_upc = None):
    return products.get_tupelo_feet(unfinished_blank, original_upc = None)

def save_finished(**kwargs):
    return products.save_finished(**kwargs)

def save_unfinished(**kwargs):
    return products.save_unfinished(**kwargs)

def save_unfinished_material(product, **kwargs):
    products.save_unfinished_material(product, **kwargs)

def save_pine(product, **kwargs):
    products.save_pine(product, **kwargs)

def save_pine_feet(product, **kwargs):
    products.save_pine_feet(product, **kwargs)

def save_tupelo(product, **kwargs):
    products.save_tupelo(product, **kwargs)

def save_tupelo_feet(product, **kwargs):
    products.save_tupelo_feet(product, **kwargs)

def remove_pine(product, **kwargs):
    products.remove_pine(product, **kwargs)

def remove_pine_feet(product, **kwargs):
    products.remove_pine_feet(product, **kwargs)

def remove_tupelo(product, **kwargs):
    products.remove_tupelo(product, **kwargs)

def remove_tupelo_feet(product, **kwargs):
    products.remove_tupelo_feet(product, **kwargs)

