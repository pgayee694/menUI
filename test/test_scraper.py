import os
import unittest
from app import app, scraper

class ScraperTest(unittest.TestCase):
    """
    Tests the functionality of the web-scraper
    """

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_parse_zomato(self):
        url = 'https://www.zomato.com/palo-alto-ca/so-gong-dong-tofu-house-palo-alto/menu'
        actual = scraper.parse_zomato(url)

        self.assertIsNotNone(actual)
        self.assertGreater(len(actual), 0)
        self.assertTrue('jpg' in actual[0].desc)
        self.assertTrue('Page 1' == actual[0].name)

        url = 'https://www.zomato.com/omaha/shucks-fish-house-oyster-bar-west-omaha/menu'
        actual = scraper.parse_zomato(url)

        self.assertIsNotNone(actual)
        self.assertGreater(len(actual), 0)
        self.assertTrue(actual[0].name == 'Lobster Stuffed Mushrooms')
        self.assertIsNotNone(actual[0].price)
        self.assertIsNotNone(actual[0].desc)