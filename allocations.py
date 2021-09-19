"""
This script will:
 + read the input files
 + perform the expense allocations from the cost centers to the accounts based on their account balances
 + write out the results to an excel spreadsheet for reporting
"""

import pandas as pd
import numpy as np
import os.path

mapfile = 'mapccs.xlsx'
calcfile = 'calculations.xlsx'
reconfile = 'recon.xlsx'

# Remove prior output files if they exist
for x in [mapfile, calcfile, reconfile]: 
    if os.path.exists(x): os.remove(x)

# Load account data
# NB:   The dataframe must have an index that uniquely identifies each row.  
#       Otherwise the joins will only pick the first row of the matching columns.
acctdf = pd.read_csv('accounts.csv')
acctdf.set_index(['month', 'product', 'channel', 'account_num'])


# Load expense data
expensedf = pd.read_csv('expenses.csv')
expensedf.set_index(['month', 'cost_center'])


# Load map
mapdf = pd.read_csv('map.csv')
mapdf.set_index(['month', 'cost_center'])

# Join map with expenses
mapccdf = pd.merge(expensedf, mapdf)
mapccdf.to_excel(mapfile)

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

# append the two dataframnes
calcdf = pd.DataFrame()
calcdf = calcdf.append(proddf)
calcdf = calcdf.append(channeldf)
calcdf.columns = ['month', 'cost_center', 'expense', 'maptype', 'product', 'account_num', 'channel', 'balance']
calcdf = calcdf.loc[:, ['month', 'cost_center', 'expense', 'maptype', 'product', 'channel', 'account_num', 'balance']]      # reorder columns

# Calculate percentages
calcdf['total_balance'] = calcdf.groupby(['month', 'cost_center'])['balance'].transform('sum')
calcdf['percent_balance'] = calcdf['balance'] / calcdf['total_balance']
calcdf['allocated_expense'] = calcdf['expense'] * calcdf['percent_balance']

# Export results
calcdf.to_excel(calcfile, sheet_name='calculations')

# Reconcile missing cost center costs (have accounts)
recondf = calcdf.loc[:,['month', 'cost_center', 'allocated_expense']]
recondf['total_cc_allocated_expense'] = calcdf.groupby(['month', 'cost_center'])['allocated_expense'].transform('sum')
recondf = recondf.drop(columns=['allocated_expense'])
recondf = recondf.drop_duplicates()
recondf = pd.merge(expensedf, recondf, on=['month', 'cost_center'], how='left', suffixes=['_expense', '_calc'])
recondf['variance'] = recondf['total_cc_allocated_expense'] - recondf['expense']
recondf.set_index(['month', 'cost_center'])
recondf.to_excel(reconfile)

