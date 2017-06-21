from django.test import TestCase
from duxdekes.util import products
from oscar.core.loading import get_model


class ProductUtilities(TestCase):
    """
    Test the product utilities set up to manage Jeff's unfinished blanks
    """
    def setUp(self):
        self.partner_class = get_model('partner', 'Partner')
        self.product_class = get_model('catalogue', 'Product')
        self.product_class_class = get_model('catalogue', 'ProductClass')


    def test_partner(self):
        partner_name = 'Dux Dekes'
        partner = products.get_partner()

        self.assertIsNotNone(partner, msg='''
        Partner class was returned
        ''')
        self.assertIsInstance(partner, self.partner_class, msg='''
        get_partner() returned an instance of the Partner class
        ''')
        self.assertEqual(partner.name, partner_name, msg='''
        Partner name matches the expected description
        ''')


    def test_product_classes(self):
        product_classes = (
                    ('Finished Decoys', products.get_finished_class()),
                    ('Instructions', products.get_instructions_class()),
                    ('Unfinished Blanks', products.get_unfinished_class()),
                )

        for name, product_class in product_classes:

            # ProductClass is returned
            self.assertIsInstance(product_class,
                self.product_class_class,
                msg='''
                    {} getter method returned an instance of ProductClass
                '''.format(name))

            # Class name matches expected name
            self.assertEqual(product_class.name,
                name,
                msg='''
                    {} ProductClass name matches the expected name
                    '''.format(name))


    def test_create_pine_product(self):
        """
        Set up a single product, with just one pine variant
        """
        pass


    def test_create_instructions_no_blank(self):
        """
        Set up a new instructions product, without a matching blank
        """
        data = {
                'price': 235.24,
                'title': 'How to paint a goose blank',
                'upc': 'TESTGOOSE1',
        }

        instructions = products.save_instructions(**data)

        self.assertIsInstance(instructions, self.product_class, msg="""
        Created instruction object is a Product
        """)
        self.assertTrue(instructions.is_parent, msg="""
        Instruction object should be a parent product
        """)
        # This test fails...?
        self.assertEqual(instructions.children.count(), 1, msg="""
        Instruction object created without associated blank should have one
        child product
        """)


    def test_create_instructions_with_blank(self):
        pass

