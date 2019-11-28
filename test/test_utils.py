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

    def test_find_cuisines(self):
        loc_id = utils.find_loc_id('Omaha', 'Nebraska')
        
        actual = utils.find_cuisines(loc_id)

        self.assertIsNotNone(actual)
        self.assertGreater(len(actual), 0)

    def test_find_establishments(self):
        loc_id = utils.find_loc_id('Omaha', 'Nebraska')

        actual = utils.find_establishments(loc_id)

        self.assertIsNotNone(actual)
        self.assertGreater(len(actual), 0)
    
    def test_search_restaurants(self):
        loc_id = utils.find_loc_id('Omaha', 'Nebraska')
        establ_ids = list(utils.find_establishments(loc_id).values())[0:2]
        cu_ids = list(utils.find_cuisines(loc_id).values())[0:2]
        cat_ids = list(utils.find_categories().values())[0:2]

        actual = utils.search_restaurants(loc_id, 'shucks', cat_ids, cu_ids, establ_ids)

        self.assertIsNotNone(actual)
        self.assertGreater(len(actual), 0)

    def test_get_restaurant_details(self):
        loc_id = utils.find_loc_id('Omaha', 'Nebraska')
        establ_ids = list(utils.find_establishments(loc_id).values())[0:2]
        cu_ids = list(utils.find_cuisines(loc_id).values())[0:2]
        cat_ids = list(utils.find_categories().values())[0:2]

        res_ids = utils.search_restaurants(loc_id, 'shucks', cat_ids, cu_ids, establ_ids)

        actual = utils.get_restaurant_details(res_ids)

        self.assertIsNotNone(actual)

    def test_list_to_string(self):
        lst = ['quack', 'le', 'doodle', 'doo']

        actual = utils.list_to_string(lst)

        self.assertEqual(actual, 'quack, le, doodle, doo')
