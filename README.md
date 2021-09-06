---
# Allocation Test
---

This set of scripts is a small project created mainly to learn how to use
Github.  It performs a trivial set of expense allocations.

The first script creates the following input files:

 1. accounts.csv = each account has a product code, a sales channel and a monthly balance
 2. expenses.csv = each cost center (e.g. a department or team code that is used to group expenses) 
   has a monthly expense amount that will be allocated to some group of accounts
 3. map.csv = map each cost center to one or more products or sales channels by month








---
# Other Notes
---

### export an environment config file:
conda env export --name allocations > allocations.yml

### create a new conda environment
conda create --name allocations



