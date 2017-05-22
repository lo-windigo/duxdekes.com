from django.test import TestCase
from duxdekes.util import products
from oscar.core.loading import get_model


class UnfinishedUtilities(TestCase):
    """
    Test the product utilities set up to manage Jeff's unfinished blanks
    """
    def setUp(self):
        self.partner_class = get_model('partner', 'Partner')
        self.product_class = get_model('catalogue', 'ProductClass')


    def test_static_entries(self):
        partner_name = 'Dux Dekes'
        unfinished_name = 'Unfinished Blanks'

        partner = products.get_partner()
        product_class = products.get_unfinished_class()

        self.assertIsNotNone(partner)
        self.assertIsNotNone(product_class)
        self.assertIsInstance(partner, self.partner_class)
        self.assertIsInstance(product_class, self.product_class)
        self.assertIs(partner.name, partner_name)
        self.assertIs(product_class.title, unfinished_name)


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
