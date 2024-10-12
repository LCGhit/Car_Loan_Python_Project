"""Retrieve fuel efficiency in mpg(miles per gallon).

Search either from offline json or from web source.
"""
import json
import re

from bs4 import BeautifulSoup

import requests  # for web scraping


def refreshedDatabase():
    """Retrieve fresh data from the source."""
    url_fuel = 'https://www.fleetnews.co.uk/news/real-world-tests\
    -reveal-cars-with-best-and-worse-mpg-fuel-economy'
    response = requests.get(url_fuel)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find_all('table')[0]  # retrieve table
    table.find('tr').decompose()
    tbody_01 = table.tbody  # retrieve body of table

    rows = tbody_01.find_all('tr')  # retrieve rows of table

    fuel_efficiency = {}
    match_make_model = '(?i:[a-z]+[\\s-][a-z0-9]*)'  # retrieve first two words
    for row in rows:
        cols = row.find_all('td')  # retrieve all columns for given row
        cleaned_key = re.match(match_make_model, cols[0].text.strip()).group(0)
        cleaned_value = int(cols[1].text.strip().
                            replace('mpg', '').replace('.', ''))
        fuel_efficiency[cleaned_key] = round(cleaned_value/10, 2)

    export = json.dumps(fuel_efficiency)
    with open('data/offline_database/fuel_efficiency.json', 'w') as f:
        f.write(export)
    return fuel_efficiency


def archivedDatabase():
    """Retrieve archived offline data."""
    with open('data/offline_database/fuel_efficiency.json', 'r') as file:
        return json.load(file)
    # return json.loads('offline_database/fuel_efficiency.json')
