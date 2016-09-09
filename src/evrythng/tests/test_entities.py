import unittest

from evrythng.entities import actions
from evrythng.entities import products


class TestProductMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product_id = products.create_product(
            name='test_creating_prod_GooeeIOT').json()['id']

    @classmethod
    def tearDownClass(cls):
        products.delete_product(
            product_id=str(cls.product_id))

    def test1_creation(self):
        ''' creating test product and check if existing name is equal to test str'''

        product_name = products.read_product(product_id=str(
            self.product_id)).json()['name']
        self.assertEqual(product_name, 'test_creating_prod_GooeeIOT')

    def test2_list(self):
        ''' creating test product and check if list's length is equal to 1'''

        self.assertEqual(
            len(products.list_products().json()), 1)

    def test3_update(self):
        ''' creating test product, update it and check,
        if product description is equal to what we expect'''

        products.update_product(product_id=str(
            self.product_id), description='test_GooeeIOT_description')
        description = products.read_product(product_id=str(
            self.product_id)).json()['description']
        self.assertEqual(description, 'test_GooeeIOT_description')


class TestActionMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product_id = products.create_product(
            name='test_creating_prod_GooeeIOT').json()['id']
        cls.action_id = actions.create_action(type_='scans',
                                          customFields={
                                              'test_custom_Field': 'test_value'},
                                          product=str(cls.product_id)).json()['id']

    @classmethod
    def tearDownClass(cls):
        products.delete_product(
            product_id=str(cls.product_id))
        actions.delete_action(
            type_='scans', action_id=str(cls.action_id))

    def test_list_actions(self):
        ''' creating test product and check if list's length is decreased'''
        self.assertEqual(len(actions.list_actions(
            type_='scans').json()), 1)


if __name__ == '__main__':
    unittest.main()
