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


# Load expense data
expensedf = pd.read_csv('expenses.csv')
expensedf.set_index(['month', 'cost_center'])


# Load map
mapdf = pd.read_csv('map.csv')
mapdf.set_index(['month', 'cost_center'])

# Join map with expenses
mapccdf = pd.merge(expensedf, mapdf)
mapccdf.to_excel('mapccs.xlsx')

# Join mapped expenses with accounts (on month and product/channel)
# get ccs mapped to products
proddf = mapccdf[mapccdf['maptype']=='product']
proddf = pd.merge(proddf, acctdf, on=['month', 'product'], how='left', suffixes=['_map', '_accts'])
proddf = proddf.drop(columns=['channel_map'])        # just says 'all'
proddf.columns = ['month', 'cost_center', 'expense', 'maptype', 'product', 'account_num', 'channel', 'balance']

# get ccs mapped to channels
channeldf = mapccdf[mapccdf['maptype']=='channel']
channeldf = pd.merge(channeldf, acctdf, on=['month', 'channel'], how='left', suffixes=['_map', '_accts'])
channeldf.reset_index()
channeldf = channeldf.drop(columns=['product_map'])        # just says 'all'
channeldf.columns = ['month', 'cost_center', 'expense', 'maptype', 'channel', 'account_num', 'product', 'balance']

# # append the two dataframnes
calcdf = pd.DataFrame()
calcdf = calcdf.append(proddf)
calcdf = calcdf.append(channeldf)
calcdf.columns = ['month', 'cost_center', 'expense', 'maptype', 'product', 'account_num', 'channel', 'balance']
calcdf = calcdf.loc[:, ['month', 'cost_center', 'expense', 'maptype', 'product', 'channel', 'account_num', 'balance']]      # reorder columns

# Calculate percentages
calcdf['total_balance'] = calcdf.groupby(['month', 'cost_center'])['balance'].transform('sum')
calcdf['percent_balance'] = calcdf['balance'] / calcdf['total_balance']
calcdf['allocated_expense'] = calcdf['expense'] * calcdf['percent_balance']

# TODO: check for missing cost center costs (have accounts)


# Export results
calcdf.to_excel('calculations.xlsx', sheet_name='calculations')
