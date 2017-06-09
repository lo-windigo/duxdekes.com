from django.test import TestCase
from duxdekes.util import products
from oscar.core.loading import get_model


class ProductUtilities(TestCase):
    """
    Test the product utilities set up to manage Jeff's unfinished blanks
    """
    def setUp(self):
        self.partner_class = get_model('partner', 'Partner')
        self.product_class = get_model('catalogue', 'ProductClass')


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
        finished_name = 'Finished Decoys'
        finished_class = products.get_finished_class()
        unfinished_name = 'Unfinished Blanks'
        unfinished_class = products.get_unfinished_class()

        self.assertIsInstance(finished_class, self.product_class, msg='''
        get_finished_class() returned an instance of ProductClass
        ''')
        self.assertIsInstance(unfinished_class, self.product_class, msg='''
        get_unfinished_class() returned an instance of ProductClass
        ''')

        self.assertEqual(finished_class.name, finished_name, msg='''
        Finished ProductClass name matches the expected class name
        ''')
        self.assertEqual(unfinished_class.name, unfinished_name, msg='''
        Unfinished ProductClass name matches the expected class name
        ''')


    def test_create_pine_product(self):
        """
        Set up a single product, with just one pine variant
        """
        pass


    def test_(self):
        pass


    def test_(self):
        pass


    def test_(self):
        pass


    def test_(self):
        pass


    def test_(self):
        pass


    def test_(self):
        pass


    def test_(self):
        pass


    def test_(self):
        pass
