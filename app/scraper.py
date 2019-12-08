import requests
from bs4 import BeautifulSoup
from app import view_models

def parse_zomato(url):

    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url=url, headers=headers)

    menu_items = []

    if response:
        soup = BeautifulSoup(response.text, 'html.parser')

        if soup.find('div', id='menu-image'):
            #time to selenium
        else:
            items = soup.find_all('div', class_='tmi-text-group')

            for item in items:
                name = item.find('div', class_='tmi-name').text.strip().split('\n')[0] if item.find('div', class_='tmi-name') else 'Mystery Meat'
                price = item.find('div', class_='tmi-price-txt').text.strip() if item.find('div', class_='tmi-price-txt') else 'Some Monies'
                desc = item.find('div', class_='tmi-desc-text').text.strip() if item.find('div', class_='tmi-desc-text') else 'Hopefully edible'

                menu_items.append(MenuItem(name, price, desc))

    return menu_items
