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

product_id = ''



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
		global product_id
		product_id = products.create_product(name='test_creating_prod_GooeeIOT', api_key=API_KEY).json()['id']
		product_name = products.read_product(product_id=str(product_id), api_key=API_KEY).json()['name']
		self.assertEqual(product_name, 'test_creating_prod_GooeeIOT')

	def test2_list(self):
		self.assertEqual(len(products.list_products(api_key=API_KEY).json()), 1)

	def test3_update(self):
		global product_id
		products.update_product(product_id=str(product_id), api_key=API_KEY, description='test_GooeeIOT_description')
		description = products.read_product(product_id=str(product_id), api_key=API_KEY).json()['description']
		self.assertEqual(description, 'test_GooeeIOT_description')

	def test4_delete(self):
		global product_id
		products.delete_product(product_id=str(product_id), api_key=API_KEY)
		self.assertEqual(len(products.list_products(api_key=API_KEY).json()), 0)



	#P.S I guess, that for all interactions with EVT platform we should come up with smth smarter than test acc
	#    according testing.
	#    

if __name__ == '__main__':
    unittest.main()



