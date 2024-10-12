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

print(car_prices)
print(fuel_efficiency)
print(maintenance_costs)
