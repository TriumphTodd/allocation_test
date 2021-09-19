"""
Create fake accounts for 9 products, 9 sales channels, 12 months, random AUM between 10**6 and 10**7
"""

import itertools
import csv
import random

products = ["p" + str(p) for p in list(range(1,10)) ]
channels = ["c" + str(c) for c in list(range(1,10)) ]
centers = ["cc" + str(cc) for cc in list(range(1,10))]
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# -------------------------------------------------------------------------------------------------
# Create account data
# -------------------------------------------------------------------------------------------------

# get cartesian product of months, products, channels and add a random account number
# and a random float for an account balance
# https://stackoverflow.com/questions/1953194/permutations-of-two-lists-in-python

accounts = []
for x in itertools.product(months, products, channels):
    accounts.append((x[0],
                     'ac' + str(random.randint(10**3, 10**4)),
                     x[1],
                     x[2],
                     float(random.randint(10**6, 10**7))))

# write out the list of tuples as a CSV file
# https://docs.python.org/3/library/csv.html
with open('accounts.csv', 'w', newline='') as csvfile:
    fieldnames = ['month', 'account_num', 'product', 'channel', 'balance']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')

    writer.writeheader()
    for x in accounts:
        writer.writerow({fieldnames[0]: x[0],
                         fieldnames[1]: x[1],
                         fieldnames[2]: x[2],
                         fieldnames[3]: x[3],
                         fieldnames[4]: x[4]})

# -------------------------------------------------------------------------------------------------
# Create expense data
# -------------------------------------------------------------------------------------------------

# get cartesian product of centers and months and add a random float for an expense number
# https://stackoverflow.com/questions/1953194/permutations-of-two-lists-in-python
expenses = []
for x in itertools.product(months, centers):
    expenses.append((x[0], x[1], float(random.randint(10**4, 10**5))))

# write out the list of tuples as a CSV file
# https://docs.python.org/3/library/csv.html
with open('expenses.csv', 'w', newline='') as csvfile:
    fieldnames = ['month', 'cost_center', 'expense']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')

    writer.writeheader()
    for x in expenses:
        writer.writerow({fieldnames[0]: x[0], fieldnames[1]: x[1], fieldnames[2]: x[2]})

# -------------------------------------------------------------------------------------------------
# Create map of cost centers to accounts
# -------------------------------------------------------------------------------------------------

# loop through cost centers, choose if it goes to products or clients (not both!!!),
#  then pick 1 to 3 of them.  Mapping is the same for each month

with open('map.csv', 'w', newline='') as csvfile:
    fieldnames = ['month', 'cost_center', 'maptype', 'product', 'channel']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
    writer.writeheader()

    maplist = []
    # write out centers
    for c in centers:
        # write in 'all' in the client field if product, vice versa
        maptype =  random.choice(['product', 'channel'])
        if maptype == 'product':
            mapdest = random.sample(products, k=random.randint(1,3))
            # create one row for each map destination with all in field 5
            for mapcc in itertools.product(months, [c], [maptype], mapdest, ['all']):
                maplist.append(mapcc)
        else:
            mapdest = random.sample(channels, k=random.randint(1,3))
            # create one row for each map destination with all in field 4
            for mapcc in itertools.product(months, [c], [maptype], ['all'], mapdest):
                maplist.append(mapcc)
    # write map
    for m in maplist:
        writer.writerow(
            {fieldnames[0]: m[0],
            fieldnames[1]: m[1],
            fieldnames[2]: m[2],
            fieldnames[3]: m[3],
            fieldnames[4]: m[4]})
