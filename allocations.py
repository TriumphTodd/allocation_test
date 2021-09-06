"""
This script will:
 + read the input files
 + perform the expense allocations from the cost centers to the accounts based on their account balances
 + write out the results to an excel spreadsheet for reporting
"""

import pandas as pd
import numpy as np

# Load account data
acctdf = pd.read_csv('accounts.csv')
acctdf.set_index(['month', 'product', 'channel'])
print('Verify balance column is numeric (float64, not object type)')
print('Data types for account data frame: ')
print(acctdf.dtypes)
print('-' * 80)

# Load expense data
expensedf = pd.read_csv('expenses.csv')
expensedf.set_index(['month', 'cost_center'])
print('Verify expense column is numeric (float64, not object type)')
print('Data types for expense data frame: ')
print(expensedf.dtypes)
print('-' * 80)

# Load map
mapdf = pd.read_csv('map.csv')
mapdf.set_index(['month', 'cost_center'])
# this will miss ccs in the map with no expenses
mapccdf = pd.merge(expensedf, mapdf, on=['month', 'cost_center'], how='left')
mapccdf.to_excel('mapccs.xlsx')

# Calculate percentages


# check for missing cost center costs (have accounts)

# Export results

