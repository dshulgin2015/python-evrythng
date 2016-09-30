import unittest
import os

from evrythng.entities import actions
from evrythng.entities import products

API_KEY = os.environ['API_KEY']


class TestProductMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Product Tests Setup"""

        cls.product_id = products.create_product(
            name='test_creating_prod_GooeeIOT', api_key=API_KEY).json()['id']

    @classmethod
    def tearDownClass(cls):
        """Product Tests Destroying"""

        products.delete_product(
            product_id=str(cls.product_id), api_key=API_KEY)

    def test_creation(self):
        """creating test product and
         check if existing name is equal to test str"""

        product_name = products.read_product(product_id=str(
            self.product_id), api_key=API_KEY).json()['name']
        self.assertEqual(product_name, 'test_creating_prod_GooeeIOT')

    def test_list(self):
        """creating test product and
         check if list's length is equal to 1"""

        self.assertEqual(
            len(products.list_products(api_key=API_KEY).json()), 1)

    def test_update(self):
        """creating test product, update it and check,
        if product description is equal to what we expect"""

        products.update_product(product_id=str(
            self.product_id), description='test_GooeeIOT_description', api_key=API_KEY)
        description = products.read_product(product_id=str(
            self.product_id), api_key=API_KEY).json()['description']
        self.assertEqual(description, 'test_GooeeIOT_description')


class TestActionMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Action Tests Setup"""

        cls.product_id = products.create_product(
            name='test_creating_prod_GooeeIOT', api_key=API_KEY).json()['id']
        cls.action_id = actions.create_action(type_='scans',
                                              customFields={
                                                  'test_custom_Field': 'test_value'},
                                        product=str(cls.product_id), api_key=API_KEY).json()['id']

    @classmethod
    def tearDownClass(cls):
        """Action Tests Destroying"""

        products.delete_product(
            product_id=str(cls.product_id), api_key=API_KEY)
        actions.delete_action(
            type_='scans', action_id=str(cls.action_id), api_key=API_KEY)

    def test_list_actions(self):
        """creating test product and
        check if list's length is decreased"""

        self.assertEqual(len(actions.list_actions(
            type_='scans', api_key=API_KEY).json()), 1)


if __name__ == '__main__':
    unittest.main()
