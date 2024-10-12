"""Retrieve monthly car maintenance costs.

Search either from offline json or from web source.
"""
import json
import re

from bs4 import BeautifulSoup

import requests  # for web scraping


def refreshedDatabase():
    """Retrieve fresh data from the source."""
    url_car_prices = 'https://www.kbb.com/car-finder/\
    ?intent=new&pricerange=0-max'
    response = requests.get(url_car_prices)
    soup = BeautifulSoup(response.content, 'html.parser')

    car_make_model = soup.find_all('a', {'class': 'css-z66djy'})
    match_make_model = '(?i:[a-z]+[\\s-][a-z0-9]*)'  # retrieve first two words
    for i in range(0, len(car_make_model)):
        car_make_model[i] = car_make_model[i].decode_contents()
        car_make_model[i] = re.search(match_make_model,
                                      car_make_model[i]).group(0)

    price = soup.find_all('div', {'class': 'css-fpbjth'})
    clean_price = []
    match_price = '(?i:[0-9]+\\,[0-9]*)'  # retrieve first two words
    for i in range(0, len(price)):
        # filter out the non price match
        try_match = re.search(match_price, str(price[i]))
        if (try_match is None):
            continue
        else:
            price[i] = price[i].decode_contents()
            clean_price.append(price[i].
                               replace(',', '').replace('$', ''))

    #  match cars with prices
    car_prices = {}
    for i in range(len(car_make_model)):
        car_prices[car_make_model[i]] = clean_price[i]

    export = json.dumps(car_prices)
    with open('data/offline_database/car_prices.json', 'w') as f:
        f.write(export)
    return car_prices


def archivedDatabase():
    """Retrieve archived offline data."""
    with open('data/offline_database/car_prices.json', 'r') as file:
        return json.load(file)
    # return json.loads('offline_database/car_prices.json')
