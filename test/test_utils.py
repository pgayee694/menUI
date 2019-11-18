import os
import unittest

from app import app, utils

class UtilsTest(unittest.TestCase):
    """
    Tests the util functions
    """

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_find_loc_id(self):
        city = 'Omaha'
        region = 'Nebraska'
        expected = 946

        actual = utils.find_loc_id(city, region)

        self.assertEqual(actual, expected)

        city = 'Brisbane'
        region = 'Queensland'
        expected = 298

        actual = utils.find_loc_id(city, region)

        self.assertEqual(actual, expected)

    def test_find_categories(self):
        actual = utils.find_categories()

        self.assertIsNotNone(actual)
        self.assertGreater(len(actual), 0)
    
    def test_get_category_id(self):
        category = [utils.find_categories()[0]]

        actual = utils.get_category_id(category)

        self.assertIsNotNone(actual)
        self.assertEqual(len(actual), 1)

    def test_find_cuisines(self):
        loc_id = utils.find_loc_id('Omaha', 'Nebraska')
        
        actual = utils.find_cuisines(loc_id)

        self.assertIsNotNone(actual)
        self.assertGreater(len(actual), 0)
    
    def test_get_cuisine_id(self):
        loc_id = utils.find_loc_id('Omaha', 'Nebraska')

        cuisine = [utils.find_cuisines(loc_id)[0]]

        actual = utils.get_cuisine_id(loc_id, cuisine)

        self.assertIsNotNone(actual)
        self.assertEqual(len(actual), 1)

    def test_find_establishments(self):
        loc_id = utils.find_loc_id('Omaha', 'Nebraska')

        actual = utils.find_establishments(loc_id)

        self.assertIsNotNone(actual)
        self.assertGreater(len(actual), 0)

    def test_get_establishment_id(self):
        loc_id = utils.find_loc_id('Omaha', 'Nebraska')
        establishment = [utils.find_establishments(loc_id)[0]]

        actual = utils.get_establishment_id(loc_id, establishment)

        self.assertIsNotNone(actual)
        self.assertEqual(len(actual), 1)
    
    def test_search_restaurants(self):
        loc_id = utils.find_loc_id('Omaha', 'Nebraska')
        establishments = utils.find_establishments(loc_id)[0:2]
        establ_ids = utils.get_establishment_id(loc_id, establishments)
        cuisines = utils.find_cuisines(loc_id)[0:2]
        cu_ids = utils.get_cuisine_id(loc_id, cuisines)
        categories = utils.find_categories()[0:2]
        cat_ids = utils.get_category_id(categories)

        actual = utils.search_restaurants(loc_id, cat_ids, cu_ids, establ_ids, 'Qdoba')
        print(actual)

        self.assertIsNotNone(actual)

    def test_list_to_string(self):
        lst = ['quack', 'le', 'doodle', 'doo']

        actual = utils.list_to_string(lst)

        self.assertEqual(actual, 'quack, le, doodle, doo')

