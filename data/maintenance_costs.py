"""Retrieve monthly car maintenance costs.

Search either from offline json or from web source.
"""
import json
import re

from bs4 import BeautifulSoup

import requests  # for web scraping


def refreshedDatabase():
    """Retrieve fresh data from the source."""
    url_maintenance = 'https://caredge.com/ranks/maintenance/'
    response = requests.get(url_maintenance)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find_all('table')[1]  # retrieve table
    tbody = table.tbody  # retrieve body of table
    rows = tbody.find_all('tr')  # retrieve rows of table

    monthly_maintenance = {}
    match_make_model = '(?i:[a-z]+[\\s-][a-z0-9]*)'  # retrieve first two words
    for row in rows:
        cols = row.find_all('td')  # retrieve all columns for given row
        cleaned_key = re.match(match_make_model, cols[1].text.strip()).group(0)
        cleaned_value = int(cols[2].text.strip().
                            replace('$', '').replace(',', ''))
        monthly_maintenance[cleaned_key] = round((cleaned_value/10)/12, 2)

    export = json.dumps(monthly_maintenance)
    with open('data/offline_database/monthly_maintenance.json', 'w') as f:
        f.write(export)
    return monthly_maintenance


def archivedDatabase():
    """Retrieve archived offline data."""
    return json.loads('data/offline_database/monthly_maintenance.json')
