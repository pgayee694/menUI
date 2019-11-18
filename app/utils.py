import requests
from app import app, view_models

def find_loc_id(city, region):
    """
    Queries Zomato API for the id of the passed in location
    """

    url = 'https://developers.zomato.com/api/v2.1/cities'
    headers = {'user_key': 'd272aea6d9f8f7183e42ea6dda828702'}
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
    headers = {'user_key': 'd272aea6d9f8f7183e42ea6dda828702'}

    response = requests.get(url, headers=headers)

    categories = []

    if response:
        body = response.json()
        for category in body['categories']:
            categories.append(category['categories']['name'])

    return categories

def get_category_id(category_names):
    """
    Queries Zomato API for the id associated with the passed in category
    """

    url = 'https://developers.zomato.com/api/v2.1/categories'
    headers = {'user_key': 'd272aea6d9f8f7183e42ea6dda828702'}

    response = requests.get(url, headers=headers)

    ids = []

    if response:
        body = response.json()
        for category in body['categories']:
            if category['categories']['name'] in category_names:
                ids.append(category['categories']['id'])

    return ids

def find_cuisines(loc_id):
    """
    Queries Zomato API for cuisines at the location id
    """

    url = 'https://developers.zomato.com/api/v2.1/cuisines'
    headers = {'user_key': 'd272aea6d9f8f7183e42ea6dda828702'}
    params = {'city_id': loc_id}

    response = requests.get(url, headers=headers, params=params)

    cuisines = []

    if response:
        body = response.json()
        for cuisine in body['cuisines']:
            cuisines.append(cuisine['cuisine']['cuisine_name'])

    return cuisines

def get_cuisine_id(loc_id, cuisine_names):
    """
    Queries Zomato API for cuisine id based off the passed in cuisine
    """

    url = 'https://developers.zomato.com/api/v2.1/cuisines'
    headers = {'user_key': 'd272aea6d9f8f7183e42ea6dda828702'}
    params = {'city_id': loc_id}

    response = requests.get(url, headers=headers, params=params)

    ids = []

    if response:
        body = response.json()
        for cuisine in body['cuisines']:
            if cuisine['cuisine']['cuisine_name'] in cuisine_names:
                ids.append(cuisine['cuisine']['cuisine_id'])

    return ids

def find_establishments(loc_id):
    """
    Queries Zomato API for estalishment types at location id
    """

    url = 'https://developers.zomato.com/api/v2.1/establishments'
    headers = {'user_key': 'd272aea6d9f8f7183e42ea6dda828702'}
    params = {'city_id': loc_id}

    response = requests.get(url, headers=headers, params=params)

    establishments = []

    if response:
        body = response.json()
        for establishment in body['establishments']:
            establishments.append(establishment['establishment']['name'])

    return establishments

def get_establishment_id(loc_id, establishment_names):
    """
    Queries Zomato API for establishment types at location id
    """

    url = 'https://developers.zomato.com/api/v2.1/establishments'
    headers = {'user_key': 'd272aea6d9f8f7183e42ea6dda828702'}
    params = {'city_id': loc_id}

    response = requests.get(url, headers=headers, params=params)

    ids = []

    if response:
        body = response.json()
        for establishment in body['establishments']:
            if establishment['establishment']['name'] in establishment_names:
                ids.append(establishment['establishment']['id'])

    return ids

def search_restaurants(loc_id, cat_ids, cu_ids, establ_ids):
    url = 'https://developers.zomato.com/api/v2.1/search'
    headers = {'user_key': 'd272aea6d9f8f7183e42ea6dda828702'}
    params = {'entity_id': loc_id, 'cuisine': list_to_string(cu_ids), 'establishment_type': list_to_string(establ_ids), 'category': list_to_string(cat_ids), 'entity_type': 'city'}

    response = requests.get(url, headers=headers, params=params)
    
    ids = []

    if response:
        body = response.json()
        for restaurant in body['restaurants']:
            ids.append(restaurant['restaurant']['R']['res_id'])

    return ids

def get_restaurant_details(res_id):
    url = 'https://developers.zomato.com/api/v2.1/restaurant'
    headers = {'user_key': 'd272aea6d9f8f7183e42ea6dda828702'}
    params = {'res_id': res_id}

    response = requests.get(url, headers=headers, params=params)

    if response:
        body = response.json()
        return view_models.Restaurant(body['name'],
        body['location']['address'],
        body['photos'][0]['photo']['url'],
        body['timings'],
        body['price_range'],
        body['user_rating']['aggregate_rating'],
        body['menu_url'])
    
    return None

def list_to_string(lst):
    if not lst:
        return ''
    
    res = ''
    string = str(lst)
    for c in string:
        if c != '[' and c != ']' and c != '\'':
            res += c

    return res