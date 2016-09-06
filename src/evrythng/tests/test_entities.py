from evrythng.entities import action_types
from evrythng.entities import actions
from evrythng.entities import applications
from evrythng.entities import application_users
from evrythng.entities import collections_
from evrythng.entities import locations
from evrythng.entities import places
from evrythng.entities import products
from evrythng.entities import projects
from evrythng.entities import properties
from evrythng.entities import thngs
import json
import unittest

with open('config.json') as configs:
    data = json.load(configs)

API_KEY = data['parameters']['API_KEY']

class TestProductMethods(unittest.TestCase):

    '''testing the following methods:

    create_product +
    list_products
    read_product +
    update_product 
    delete_product 

    on a test EVT account by Dmitry Shulgin.

    '''

    def test1_creation(self):
        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT', api_key=API_KEY).json()['id']
        product_name = products.read_product(product_id=str(
            product_id), api_key=API_KEY).json()['name']
        self.assertEqual(product_name, 'test_creating_prod_GooeeIOT')
        products.delete_product(product_id=str(product_id), api_key=API_KEY)

    def test2_list(self):
        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT', api_key=API_KEY).json()['id']
        self.assertEqual(
            len(products.list_products(api_key=API_KEY).json()), 1)
        products.delete_product(product_id=str(product_id), api_key=API_KEY)

    def test3_update(self):
        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT', api_key=API_KEY).json()['id']
        products.update_product(product_id=str(
            product_id), api_key=API_KEY, description='test_GooeeIOT_description')
        description = products.read_product(product_id=str(
            product_id), api_key=API_KEY).json()['description']
        self.assertEqual(description, 'test_GooeeIOT_description')
        products.delete_product(product_id=str(product_id), api_key=API_KEY)

    def test4_delete(self):
        count = len(products.list_products(api_key=API_KEY).json())
        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT', api_key=API_KEY).json()['id']
        count += 1
        status_code = products.delete_product(
            product_id=str(product_id), api_key=API_KEY).status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(len(products.list_products(
            api_key=API_KEY).json()), count - 1)


class TestActionMethods(unittest.TestCase):

    '''testing the following methods:

    create_action+
    delete_action+
    list_actions

    on a test EVT account by Dmitry Shulgin.

    '''

    def test1_(self):

        # creating necessary objects required for making test action: thng ||
        # product || shortID
        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT', api_key=API_KEY).json()['id']
        # getting action id from response object
        action_id = actions.create_action(type_='scans',  # need to create more on every base action types.
                                          api_key=API_KEY,
                                          customFields={
                                              'test_custom_Field': 'test_value'},
                                          product=str(product_id)).json()['id']
        # checking if status code == 200
        status_code = actions.delete_action(type_='scans', action_id=str(
            action_id), api_key=API_KEY).status_code  # why we need type when we know action id?
        self.assertEqual(status_code, 200)
        products.delete_product(product_id=str(product_id), api_key=API_KEY)

    def test2_list_actions(self):
        # save number of actions before we create new one.
        count = len(actions.list_actions(
            type_='scans', api_key=API_KEY).json())

        # creating necessary objects required for making test action: thng ||
        # product || shortID
        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT', api_key=API_KEY).json()['id']
        action_id = actions.create_action(type_='scans',
                                          api_key=API_KEY,
                                          customFields={
                                              'test_custom_Field': 'test_value'},
                                          product=str(product_id)).json()['id']
        self.assertEqual(len(actions.list_actions(
            type_='scans', api_key=API_KEY).json()), count + 1)

        # delete test objects
        actions.delete_action(
            type_='scans', action_id=str(action_id), api_key=API_KEY)
        products.delete_product(product_id=str(product_id), api_key=API_KEY)


if __name__ == '__main__':
    unittest.main()
