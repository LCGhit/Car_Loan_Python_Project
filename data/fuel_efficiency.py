"""Retrieve fuel efficiency in mpg(miles per gallon).

Search either from offline json or from web source.
"""
import json
import re

from bs4 import BeautifulSoup

import requests  # for web scraping


def refreshedDatabase():
    """Retrieve fresh data from the source."""
    url_fuel = 'https://www.fueleconomy.gov/feg/byfuel/Hybrid2024.shtml'
    response = requests.get(url_fuel)
    soup = BeautifulSoup(response.content, 'html.parser')

    # retrieve car make and model
    rows = soup.find_all('a', {'class': 'ymm'})
    car_make_model = []
    match_make_model = '(?i:[a-z]+[\\s-][a-z0-9]*)'  # retrieve first two words
    for i in range(len(rows)):
        car_make_model.append(rows[i])
        car_make_model[i] = car_make_model[i].decode_contents()
        car_make_model[i] = re.search(match_make_model,
                                      car_make_model[i]).group(0).upper()

    # retrieve mpg
    # change miles per gallon to kilometers per liter (rounded)
    mpg_raw_data = soup.find_all('div', {'class': 'mpgSummary'})
    mpg = []
    km_per_liter = (1609344/3785412)
    for i in range(len(mpg_raw_data)):
        mpg.append(re.search('[0-9]+', mpg_raw_data[i].text).group(0))
        mpg[i] = round(int(mpg[i])*km_per_liter, 2)

    # match car name with mpg
    fuel_efficiency = {}
    for i in range(0, len(mpg)):
        fuel_efficiency[car_make_model[i]] = mpg[i]

    export = json.dumps(fuel_efficiency)
    with open('data/offline_database/fuel_efficiency.json', 'w') as f:
        f.write(export)
    return fuel_efficiency


def archivedDatabase():
    """Retrieve archived offline data."""
    with open('data/offline_database/fuel_efficiency.json', 'r') as file:
        return json.load(file)
