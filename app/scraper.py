import requests
from bs4 import BeautifulSoup
import re
import json
from app import view_models


def parse_zomato(url):

    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url='https://www.zomato.com/omaha/salween-thai-omaha/menu', headers=headers)

    menu_items = []

    if response:
        soup = BeautifulSoup(response.text, 'html.parser')

        if soup.find('div', id='menu-image'):
            #menu is a picture(s)
            json_string = soup.find(text=re.compile('menuPages')).strip().split('\n')[1].strip().split()[2][:-1]
            json_obj = json.loads(json_string)
            for i in range(len(json_obj)):
                menu_items.append(MenuItem('Page {}'.format(i), None, json_obj[i]['url'].strip()))
        else:
            #menu is just a page
            items = soup.find_all('div', class_='tmi-text-group')

            for item in items:
                name = item.find('div', class_='tmi-name').text.strip().split('\n')[0] if item.find('div', class_='tmi-name') else 'Mystery Meat'
                price = item.find('div', class_='tmi-price-txt').text.strip() if item.find('div', class_='tmi-price-txt') else 'Some Monies'
                desc = item.find('div', class_='tmi-desc-text').text.strip() if item.find('div', class_='tmi-desc-text') else 'Hopefully edible'

                menu_items.append(MenuItem(name, price, desc))

    return menu_items
