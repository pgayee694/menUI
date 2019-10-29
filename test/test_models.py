import os
import unittest

from app import app, models, db
from config import basedir


class ModelsTest(unittest.TestCase):
    """
    Tests for the models
    """

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        u = models.User(username='test', password='asdf', location='nyc')
        db.session.add(u)
        db.session.commit()

        users = models.User.query.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, 'test')
    
    def test_restaurant(self):
        r = models.Restaurant(name='test')
        db.session.add(r)
        db.session.commit()

        rs = models.Restaurant.query.all()
        self.assertEqual(len(rs), 1)
        self.assertEqual(rs[0].name, 'test')

    def test_user_restaurants(self):
        u = models.User(username='test', password='asdf', location='nyc')
        r = models.Restaurant(name='test')
        user_restaurant = models.User_Restaurants(user_id=u.id, restaurant_id=r.id)
        db.session.add(user_restaurant)
        db.session.commit()

        user_restaurants = models.User_Restaurants.query.all()
        self.assertEqual(len(user_restaurants), 1)
        self.assertEqual(user_restaurants[0].user_id, u.id)
        self.assertEqual(user_restaurants[0].restaurant_id, r.id)
    
    def test_friends(self):
        u1 = models.User(username='test1', password='asdf1', location='nyc')
        u2 = models.User(username='test2', password='asdf2', location='nyc')
        friendship = models.Friends(friend1_id=u1.id, friend2_id=u2.id)
        db.session.add(friendship)
        db.session.commit()

        friendships = models.Friends.query.all()
        self.assertEqual(len(friendships), 1)
        self.assertEqual(friendships[0].friend1_id, u1.id)
        self.assertEqual(friendships[0].friend2_id, u2.id)
