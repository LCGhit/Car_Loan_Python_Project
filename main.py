"""User interface and main functions."""

import data.car_prices
import data.fuel_efficiency
import data.maintenance_costs


# Download fresh data from sources.
# In case of error, retrieve data from local files.
car_prices = []
fuel_efficiency = []
maintenance_costs = []
try:
    car_prices = data.car_prices.refreshedDatabase()
except Exception:
    car_prices = data.car_prices.archivedDatabase()

try:
    fuel_efficiency = data.fuel_efficiency.refreshedDatabase()
except Exception:
    fuel_efficiency = data.fuel_efficiency.archivedDatabase()

try:
    maintenance_costs = data.maintenance_costs.refreshedDatabase()
except Exception:
    maintenance_costs = data.maintenance_costs.archivedDatabase()

#  dictionary with cars for which there is data
car_options = {}
for key, value in car_prices.items():
    temporary_dict = {}
    try:
        temporary_dict['car price'] = value
        temporary_dict['maintenance cost'] = maintenance_costs[key]
        temporary_dict['fuel efficiency'] = fuel_efficiency[key]
        car_options[key] = temporary_dict
    except Exception:
        continue

print(len(car_options))


def mainFunc():
    """Initiate program with menu."""


if __name__ == '__main__':
    mainFunc()
