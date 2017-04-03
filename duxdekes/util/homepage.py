
from oscar.core.loading import get_model

def homepage_data(category_name):

    Category = get_model('catalogue', 'Category')
    Product = get_model('catalogue', 'Product')

    parent_category = Category.objects.get(name=category_name)
    categories = parent_category.get_descendants_and_self()

    # Get the newest products from each category tree
    products = []
    for this_category in categories:
        #products.append(this_category.product_set.browsable.order_by('-date_updated')[:4])
        products.extend(Product.objects.filter(
            categories__in=[this_category,]
        ).order_by('-date_updated')[:4])

    latest_products = sorted(products,
        key=lambda product: product.date_updated,
        reverse=True)

    return {
        'products': latest_products[:4],
        'categories': categories,
    }
