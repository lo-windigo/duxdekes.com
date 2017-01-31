import csv, re
from products.models import Product


class MapException(Exception):
    pass


#def save_category(data):
#    """
#    Map a CSV line to a category
#    """
#    map = {
#            'categoryid': '',
#            'category': '',
#            }
#
#    try:
#        map_csv_to_object(data, mapping)
#    except MapException e:
#        pass
    

def save_product(data):
    """
    Map a CSV line to a product
    """

    col_map = {
            'product_id': 0,
            'description': 1,
            'base_price': 3,
            'hidden': 6,
            }
    id_in_description = re.compile(r"([A-Z0-9 ]+)\s+-\s+")


    try:
        # Conver the hidden field to a boolean value
        data[col_map['hidden']] = data[col_map['hidden']] == 'True'

        # Clean up the product description
        if data[col_map['description']]:

            # Trim any leading or trailing whitespace
            desc = data[col_map['description']].strip()
            
            # Pull the product ID out of the description, if present
            id_match = id_in_description.match(desc)
            
            if id_match:
                product_id = id_match.group(1)
                full_match = id_match.group(0)

                # Trim off ID from the description
                desc = desc[len(full_match):]

                # Save the product ID if it isn't present yet
                if not data[col_map['product_id']]:
                    data[col_map['product_id']] = product_id

            data[col_map['description']] = desc.title()

        map_csv_to_object(data, Product(), col_map)

    except (MapException, Exception) as e:
        print('Ran into an exception: {}'.format(e))


def map_csv_to_object(data, model, mapping):
    """
    Take a line of input from a CSV file, and map it to a Django model
    """
    for member, index in mapping.items():
        setattr(model, member, data[index])

    model.save()


def import_data():
    """
    Import data from the various CSV files
    """

    # Products
    product_file_path = '/home/windigo/code/duxdekes/resources/products.csv'

    with open(product_file_path) as product_file:
        product_import = csv.reader(product_file)
        
        for product_data in product_import:
            save_product(product_data)


if __name__ == "__main__":
    import_data()

