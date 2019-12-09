import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures as cf
from requests_futures.sessions import FuturesSession
from app import app, view_models, models, db

def find_loc_id(city, region):
    """
    Queries Zomato API for the id of the passed in location
    """

    url = 'https://developers.zomato.com/api/v2.1/cities'
    headers = {'user_key': 'e74153df38632880474d4788e0936560'}
    params = {'q': '{}, {}'.format(city, region)}
    
    response = requests.get(url, headers=headers, params=params)

    if response:
        body = response.json()
        for location in body['location_suggestions']:
            if city in location['name'] and location['state_name'] == region:
                return location['id']
        else:
            app.logger.error('No location named {} found'.format(params['q']))
            return None
    else:
        app.logger.error('No locations found for {}'.format(params['q']))
        return None

def find_categories():
    """
    Queries Zomato API for categories of restaurants
    """

    url = 'https://developers.zomato.com/api/v2.1/categories'
    headers = {'user_key': 'e74153df38632880474d4788e0936560'}

    response = requests.get(url, headers=headers)

    categories = {}

    if response:
        body = response.json()
        for category in body['categories']:
            categories[category['categories']['name']] = category['categories']['id']

    return categories

def find_cuisines(loc_id):
    """
    Queries Zomato API for cuisines at the location id
    """

    url = 'https://developers.zomato.com/api/v2.1/cuisines'
    headers = {'user_key': 'e74153df38632880474d4788e0936560'}
    params = {'city_id': loc_id}

    response = requests.get(url, headers=headers, params=params)

    cuisines = {}

    if response:
        body = response.json()
        for cuisine in body['cuisines']:
            cuisines[cuisine['cuisine']['cuisine_name']] = cuisine['cuisine']['cuisine_id']

    return cuisines

def find_establishments(loc_id):
    """
    Queries Zomato API for estalishment types at location id
    """

    url = 'https://developers.zomato.com/api/v2.1/establishments'
    headers = {'user_key': 'e74153df38632880474d4788e0936560'}
    params = {'city_id': loc_id}

    response = requests.get(url, headers=headers, params=params)

    establishments = {}

    if response:
        body = response.json()
        for establishment in body['establishments']:
            establishments[establishment['establishment']['name']] = establishment['establishment']['id']

    return establishments

def search_restaurants(loc_id, res_name, cat_ids, cu_ids, establ_ids, connection_session=None):
    url = 'https://developers.zomato.com/api/v2.1/search'
    headers = {'user_key': 'e74153df38632880474d4788e0936560'}
    params = {'entity_id': loc_id, 'q': res_name, 'cuisine': list_to_string(cu_ids), 'establishment_type': list_to_string(establ_ids), 'category': list_to_string(cat_ids), 'entity_type': 'city'}

    response = connection_session.get(url, headers=headers, params=params) if connection_session else requests.get(url, headers=headers, params=params)
    
    ids = []

    if response:
        body = response.json()
        for restaurant in body['restaurants']:
            ids.append(restaurant['restaurant']['R']['res_id'])

    return ids

def get_restaurant_details(res_ids):
    url = 'https://developers.zomato.com/api/v2.1/restaurant'
    headers = {'user_key': 'e74153df38632880474d4788e0936560'}

    restaurants = []

    session = FuturesSession()
    futures = []

    for res_id in res_ids:
        params = {'res_id': res_id}
        futures.append(session.get(url, headers=headers, params=params))

    for future in cf.as_completed(futures):
        response = future.result()

        if response:
            body = response.json()
            try:
                restaurants.append(view_models.Restaurant(body['name'],
                body['location']['address'],
                body['photos'][0]['photo']['url'],
                body['timings'],
                body['price_range'],
                body['user_rating']['aggregate_rating'],
                body['menu_url']))
            except KeyError:
                restaurants.append(view_models.Restaurant(body['name'],
                body['location']['address'],
                '', # randomly zomato just doesn't have photos
                body['timings'],
                body['price_range'],
                body['user_rating']['aggregate_rating'],
                body['menu_url']))
    
    return restaurants

def list_to_string(lst):
    if not lst:
        return ''
    
    res = ''
    string = str(lst)
    for c in string:
        if c != '[' and c != ']' and c != '\'':
            res += c

    return res
	
def add_user_restaurant(user_id, restaurant_name):
	restaurant = add_restaurant(restaurant_name)
	user_restaurant = models.UserRestaurant.query.filter_by(user_id=user_id, restaurant_id=restaurant).first()
	
	if not user_restaurant:
		user_restaurant = models.UserRestaurant(user_id=user_id, restaurant_id=restaurant)
		db.session.add(user_restaurant)
		db.session.commit()
	
	return user_restaurant.id
	
def add_restaurant(restaurant_name):
	restaurant = models.Restaurant.query.filter_by(name=restaurant_name).first()
	
	if not restaurant:
		restaurant = models.Restaurant(name=restaurant_name)
		db.session.add(restaurant)
		db.session.commit()
	
	return restaurant.id

#returns the first user with the given username, None if the user isn't found.
def find_user_by_username(username_in):
    return models.User.query.filter_by(username=username_in).first()

def find_friendship(id1, id2):
    return models.Friends.query.filter_by(friend1_id=id1, friend2_id=id2).first()
