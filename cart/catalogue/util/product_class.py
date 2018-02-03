from oscar.core.loading import get_model


def make_class_attributes():
    """
    Create attributes required for shipping with UPS/Dux Dekes
    """
    ProductAttribute = get_model('catalogue', 'ProductAttribute')
    ProductClass = get_model('catalogue', 'ProductClass')

    for product_class in ProductClass.objects.all():
        ProductAttribute.objects.get_or_create(code='weight',
                product_class=product_class,
                defaults={
                    'name': 'Weight',
                    'type': ProductAttribute.FLOAT,
                    })
        ProductAttribute.objects.get_or_create(code='box',
                product_class=product_class,
                defaults={
                    'name': 'Box used for shipping',
                    'type': ProductAttribute.ENTITY,
                    })

