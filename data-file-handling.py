# I want to store the data using classes and file handling
# create different files to store for different lists

import pandas as pd

df = pd.read_csv('inventory-list.csv')
print(df) #prints the entire dataframe

df.at[0, 'Item Name'] = 'chicken'
df.at[0, 'Quantity'] = 2
df.at[0, 'Expiration Date'] = '111626'
print(df)