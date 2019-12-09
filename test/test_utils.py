import os
import unittest

from app import app, utils, models, db

class UtilsTest(unittest.TestCase):
    """
    Tests the util functions
    """

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

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

        actual = utils.search_restaurants(loc_id, ['shucks'], cat_ids, cu_ids, establ_ids)

        self.assertIsNotNone(actual)
        self.assertGreater(len(actual), 0)

    def test_get_restaurant_details(self):
        loc_id = utils.find_loc_id('Omaha', 'Nebraska')
        establ_ids = list(utils.find_establishments(loc_id).values())[0:2]
        cu_ids = list(utils.find_cuisines(loc_id).values())[0:2]
        cat_ids = list(utils.find_categories().values())[0:2]

        res_ids = utils.search_restaurants(loc_id, ['shucks'], cat_ids, cu_ids, establ_ids)

        actual = utils.get_restaurant_details(res_ids)

        self.assertIsNotNone(actual)

    def test_list_to_string(self):
        lst = ['quack', 'le', 'doodle', 'doo']

        actual = utils.list_to_string(lst)

        self.assertEqual(actual, 'quack, le, doodle, doo')

    def test_union_restaurants(self):
        db.create_all()
        user1 = models.User(id=1, username='test1', password='1', location_id=1)
        user2 = models.User(id=2, username='test2', password='1', location_id=1)
        user3 = models.User(id=3, username='test3', password='1', location_id=1)
        users = {user1, user2, user3}

        user_restaurant1 = models.UserRestaurant(id=1, user_id=1, restaurant_id=1)
        user_restaurant2 = models.UserRestaurant(id=2, user_id=1, restaurant_id=2)
        user_restaurant3 = models.UserRestaurant(id=3, user_id=2, restaurant_id=2)
        user_restaurant4 = models.UserRestaurant(id=4, user_id=3, restaurant_id=2)
        user_restaurant5 = models.UserRestaurant(id=5, user_id=3, restaurant_id=3)

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user_restaurant1)
        db.session.add(user_restaurant2)
        db.session.add(user_restaurant3)
        db.session.add(user_restaurant4)
        db.session.add(user_restaurant5)
        db.session.commit()

        actual = utils.union_restaurants(users)
        self.assertEqual(actual, {1, 2, 3})

    def test_intersection_restaurants(self):
        db.create_all()
        user1 = models.User(id=4, username='test1', password='1', location_id=1)
        user2 = models.User(id=5, username='test2', password='1', location_id=1)
        user3 = models.User(id=6, username='test3', password='1', location_id=1)
        users = {user1, user2, user3}

        user_restaurant1 = models.UserRestaurant(id=6, user_id=4, restaurant_id=4)
        user_restaurant2 = models.UserRestaurant(id=7, user_id=4, restaurant_id=5)
        user_restaurant3 = models.UserRestaurant(id=8, user_id=5, restaurant_id=5)
        user_restaurant4 = models.UserRestaurant(id=9, user_id=6, restaurant_id=5)
        user_restaurant5 = models.UserRestaurant(id=10, user_id=6, restaurant_id=6)
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user_restaurant1)
        db.session.add(user_restaurant2)
        db.session.add(user_restaurant3)
        db.session.add(user_restaurant4)
        db.session.add(user_restaurant5)
        db.session.commit()

        actual = utils.intersection_restaurants(users)
        self.assertEqual(actual, {5})
    
    def test_get_user_restaurants(self):
        db.create_all()
        user1 = models.User(username='test1', password='1', location_id=1)
        db.session.add(user1)
        db.session.commit()

        res1 = models.Restaurant(name='Qdoba')
        res2 = models.Restaurant(name='Salween Thai')
        db.session.add(res1)
        db.session.add(res2)
        db.session.commit()

        user_res1 = models.UserRestaurant(user_id=user1.id, restaurant_id=res1.id)
        user_res2 = models.UserRestaurant(user_id=user1.id, restaurant_id=res2.id)
        db.session.add(user_res1)
        db.session.add(user_res2)
        db.session.commit()

        actual = utils.get_user_restaurants(user1.id)

        self.assertEqual(len(actual), 2)
