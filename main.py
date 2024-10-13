"""User interface and main functions."""

import data.car_prices
import data.fuel_efficiency
import data.maintenance_costs


def retrieveScrapedData(module):
    """Return data from given scrapper module.

    Download fresh data from source.
    In case of error, retrieve data from local file.
    """
    result = ''
    try:
        result = module.refreshedDatabase()
    except Exception:
        result = module.archivedDatabase()
    return result


def matchDictionaries(keys, dict_array):
    """Combine three dictionaries.

    Include only entries present in all three dictionaries.
    """
    complete_dict = {}
    for key in keys:
        temporary_dict = {}
        try:
            temporary_dict['car price'] = dict_array[0][key]
            temporary_dict['fuel efficiency'] = dict_array[1][key]
            temporary_dict['maintenance cost'] = dict_array[2][key]
            complete_dict[key] = temporary_dict
        # if any data is missing for a car model, skip it
        except Exception:
            continue
    return complete_dict


def validateNum(start, end, message):
    """Validate number from range(start, end)."""
    flag = 'y'
    result = 0
    while (flag == 'y'):
        user_input = input(message)
        user_input = user_input.strip().lower()
        if (user_input.isdigit()):
            if (int(user_input) in range(start, end)):
                result = float(user_input)
                flag = 'n'
            else:
                print(f'Out of range. Insert a number from {start} to {end-1}')
        else:
            print('Invalid input. Enter a number, please.')
    return result


def pickDictKey(myDict, message):
    """Show dictionary keys and return JUST the picked KEY."""
    dict_keys = list(myDict.keys())
    for i in range(len(dict_keys)):
        print(f'{i+1}. {dict_keys[i]}')
    selection = validateNum(1, len(list(myDict))+1, message)
    return dict_keys[int(selection)-1]


def monthlyPaymentCalc(price, downpayment, loan_period):
    """Calculate and return monthly payment."""
    annual_interest_rate = 0.0499
    monthly_interest_rate = annual_interest_rate/12
    monthly_payment = ((int(price)-downpayment)*(monthly_interest_rate)
                       * ((1+monthly_interest_rate) ** loan_period))\
        / (((1+monthly_interest_rate) ** loan_period) - 1)
    return round(monthly_payment, 2)


def reduceDict(myDict, key):
    """Return dictionary without given entry."""
    myDict_copy = myDict.copy()
    del myDict_copy[key]
    return myDict_copy


def monthlyGasSpending(monthly_distance, fuel_efficiency,  price_gas_liter):
    """Return calculation of monthly spending on gas."""
    result = (monthly_distance / fuel_efficiency) * price_gas_liter
    return round(result, 2)


def compareCarsCosts(myDict):
    """Compare cars expenses.

    Suggest the best option according to comparison.
    """
    totals = {}
    for key in myDict.keys():
        totals[key] = 0
        print('\n', key)
        for key_02, value in myDict[key].items():
            print(f'{key_02}: {value}€')
            totals[key] += value
        print(f'TOTAL: {round(totals[key], 2)}€')

    totals_keys = list(totals.keys())
    suggestion = ''
    if (totals[totals_keys[0]] > totals[totals_keys[1]]):
        suggestion = totals_keys[1]
    else:
        suggestion = totals_keys[0]
    print('After analysing the data, '
          + f'we would suggest purchasing {suggestion}')


def mainFunc():
    """Initiate program with menu."""
    # put relevant scrapped data into dictionary
    car_prices = retrieveScrapedData(data.car_prices)
    fuel_efficiency = retrieveScrapedData(data.fuel_efficiency)
    maintenance_costs = retrieveScrapedData(data.maintenance_costs)
    car_options = matchDictionaries(car_prices.keys(),
                                    [car_prices,
                                     fuel_efficiency,
                                     maintenance_costs])

    # relevant user input
    first_car = pickDictKey(car_options,
                            "Pick a car you're interested in => ")
    second_car = pickDictKey(reduceDict(car_options, first_car),
                             "Pick another car you're interested in => ")

    price_gas_liter = 1.5
    km_per_week = validateNum(0, 5000,
                              'How many kilometers per week '
                              + 'do you drive on average? => ')
    downpayment_percent = validateNum(0, 21,
                                      'How much would you like to pay upfront?'
                                      + '\n(percentage: 0 to 20) => ')/100
    loan_period = validateNum(36, 85,
                              'How long will you take to pay the loan?\n'
                              + '(timeframe 36 to 85 months) => ')

    # compute and aggregate info for each chosen car in dictionary
    cars_expenses = {first_car: {}, second_car: {}}
    for car in cars_expenses:
        cars_expenses[car]['monthly loan payment'] = monthlyPaymentCalc(
            car_options[car]['car price'],
            downpayment_percent*float(car_options[car]['car price']),
            loan_period)

        cars_expenses[car]['maintenance cost'] =\
            car_options[car]['maintenance cost']

        cars_expenses[car]['monthly gas spending'] = monthlyGasSpending(
            km_per_week*4,
            car_options[car]['fuel efficiency'],
            price_gas_liter)

    # show comparison between each cars expenses
    compareCarsCosts(cars_expenses)


if __name__ == '__main__':
    mainFunc()
