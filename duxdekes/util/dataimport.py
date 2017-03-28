import csv, re
from oscar.core.loading import get_model
from django.db.utils import IntegrityError


__all__ = ['import_data',]



def save_category(data, parents):
    """
    Map a CSV line to a category
    """
    CATEGORY_TYPE = 0
    DESCRIPTION = 1
    CATEGORY_PRODUCTS = 2

    Category = get_model('catalogue', 'Category')
    ProductCategory = get_model('catalogue', 'ProductCategory')
    StockRecord = get_model('partner', 'StockRecord')

    # Treebeard uses raw SQL, so we can't rely on object methods
    get = lambda node_id: Category.objects.get(pk=node_id)

    try:
        # Add this category to its parent category
        category = get(
            parents[data[CATEGORY_TYPE]]
        ).add_child(name=data[DESCRIPTION])

    except Exception as e:
        print('Ran into a category exception: {}'.format(e))
        return

    # Add product to this category
    for connected_id in data[CATEGORY_PRODUCTS].split(', '):
        try:
            for stock in StockRecord.objects.filter(partner_sku=connected_id):
                productCategoryRelation = ProductCategory()
                productCategoryRelation.product = stock.product
                productCategoryRelation.category = category
                productCategoryRelation.save()

        except Exception as e:
            print('Could not add product to category: {}'.format(e))

    

def save_product(data, categories, provider, product_class):
    """
    Map a CSV line to a product
    """

    PRODUCT_ID = 0
    DESCRIPTION = 1
    BASE_PRICE = 3

    id_in_description = re.compile(r"([A-Z0-9 ]+)\s+-\s+")
    Category = get_model('catalogue', 'Category')
    Product = get_model('catalogue', 'Product')
    StockRecord = get_model('partner', 'StockRecord')

    # Treebeard uses raw SQL, so we can't rely on object methods
    get = lambda node_id: Category.objects.get(pk=node_id)

    #try:
    # Clean up the product description
    if not data[DESCRIPTION]:
        return

    # Trim any leading or trailing whitespace
    desc = data[DESCRIPTION].strip()
    
    # Pull the product ID out of the description, if present
    id_match = id_in_description.match(desc)
    
    if id_match:
        product_id = id_match.group(1)
        full_match = id_match.group(0)

        # Trim off ID from the description
        desc = desc[len(full_match):]

        # Save the product ID if it isn't present yet
        if not data[PRODUCT_ID]:
            data[PRODUCT_ID] = product_id

    if not data[PRODUCT_ID]:
        return

    data[DESCRIPTION] = desc.title()

    # Create a product, assuming its an unfinished blank
    product = Product()
    product.title = data[DESCRIPTION]
    product.structure = Product.PARENT
    product.product_class = product_class
    product.save()

    pine = Product()
    pine.title = 'Pine'
    pine.structure = Product.CHILD
    pine.parent = product
    pine.save()

    stock = StockRecord()
    stock.product = pine
    stock.partner = provider
    stock.partner_sku = data[PRODUCT_ID]
    stock.price_excl_tax = data[BASE_PRICE]
    stock.save()

    #except Exception as e:
    #    print('Ran into a product exception: {}'.format(e))


def import_data():
    import_csv_data(*import_static_data())


def import_csv_data(provider, product_class, base_categories):
    """
    Import data from the various CSV files
    """

    # Products
    product_file_path = '/home/windigo/code/duxdekes/resources/products.csv'

    with open(product_file_path) as product_file:
        product_import = csv.reader(product_file)
        
        for product_data in product_import:
            try:
                save_product(product_data, base_categories, provider, product_class)
            except IntegrityError as e:
                print('IntegrityError, most likely duplicate key: {}'.format(e))

    # Categories
    category_file_path = '/home/windigo/code/duxdekes/resources/categories.csv'

    with open(category_file_path) as category_file:
        category_import = csv.reader(category_file)
        
        for category_data in category_import:
            save_category(category_data, base_categories)


def import_static_data():

    Category = get_model('catalogue', 'Category')
    Partner = get_model('partner', 'Partner')
    ProductClass = get_model('catalogue', 'ProductClass')

    # Treebeard uses raw SQL, so we can't rely on object methods
    get = lambda node_id: Category.objects.get(pk=node_id)

    # Set up Jeff as a provider
    jeff = Partner(name="Dux Dekes")
    jeff.save()

    # Set up a default product class
    product_class = ProductClass()
    product_class.name = 'Product'
    product_class.requires_shipping = False
    product_class.save()

    unfinished = Category.add_root(name='Unfinished Blanks')
    finished = get(unfinished.pk).add_sibling(name='Finished Decoys')
    instructions = get(unfinished.pk).add_sibling(name='Instructions')
    default_import = get(unfinished.pk).add_sibling(name='Imported Data')

    # Set up the main four (three) categories, and save them to a dict
    categories = {
        'u': unfinished.pk,
        'f': finished.pk,
        'i': instructions.pk,
        'x': default_import.pk,
    }

    return jeff, product_class, categories


if __name__ == "__main__":
    import_data()

