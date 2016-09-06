from evrythng.entities import actions
from evrythng.entities import products
import unittest


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
        ''' creating test product and check if existing name is equal to test str'''

        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT').json()['id']
        product_name = products.read_product(product_id=str(
            product_id)).json()['name']
        self.assertEqual(product_name, 'test_creating_prod_GooeeIOT')
        products.delete_product(product_id=str(product_id))

    def test2_list(self):
        ''' creating test product and check if list's length is equal to 1'''

        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT').json()['id']
        self.assertEqual(
            len(products.list_products().json()), 1)
        products.delete_product(product_id=str(product_id))

    def test3_update(self):
        ''' creating test product, update it and check, if product description is equal to what we expect'''

        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT').json()['id']
        products.update_product(product_id=str(
            product_id), description='test_GooeeIOT_description')
        description = products.read_product(product_id=str(
            product_id)).json()['description']
        self.assertEqual(description, 'test_GooeeIOT_description')
        products.delete_product(product_id=str(product_id))

    def test4_delete(self):
        ''' creating test product and check, if status code of deletion == 200 and
         length of list is equal to what we expect'''

        count = len(products.list_products().json())
        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT').json()['id']
        count += 1
        status_code = products.delete_product(
            product_id=str(product_id)).status_code
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
        ''' creating test product and check, if status code of deletion == 200'''

        # creating necessary objects required for making test action: thng ||
        # product || shortID
        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT').json()['id']
        # getting action id from response object
        action_id = actions.create_action(type_='scans',
                                          customFields={
                                              'test_custom_Field': 'test_value'},
                                          product=str(product_id)).json()['id']
        # checking if status code == 200
        status_code = actions.delete_action(type_='scans', action_id=str(
            action_id)).status_code  # why we need type when we know action id?
        self.assertEqual(status_code, 200)
        products.delete_product(product_id=str(product_id))

    def test2_list_actions(self):
        ''' creating test product and check if list's length is decreased'''

        # save number of actions before we create new one.
        count = len(actions.list_actions(
            type_='scans').json())

        # creating necessary objects required for making test action: thng ||
        # product || shortID
        product_id = products.create_product(
            name='test_creating_prod_GooeeIOT').json()['id']
        action_id = actions.create_action(type_='scans',
                                          customFields={
                                              'test_custom_Field': 'test_value'},
                                          product=str(product_id)).json()['id']
        self.assertEqual(len(actions.list_actions(
            type_='scans').json()), count + 1)

        # delete test objects
        actions.delete_action(
            type_='scans', action_id=str(action_id))
        products.delete_product(product_id=str(product_id))


if __name__ == '__main__':
    unittest.main()
