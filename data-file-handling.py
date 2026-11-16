# I want to store the data using classes and file handling
# create different files to store for different lists

import pandas as pd

continueList = "Y"

df = pd.read_csv('inventory-list.csv')
print(df) #prints the entire dataframe

# checks if the fridge/inventory list is eempty
if df.empty:
    print("Your Inventory is empty.")

# user is prompted to add items to list
print("Enter the name of the item, the quanity, and expiration date (FORMAT MMDDYY), and category: ")


# while loop that allows user to continue to enter values until they are finished
# a way to check if an index is empty
while continueList == "Y" :
    items = input("Enter the name of the item")

    # create a dictionary for each food entry
    # convert dictionary to dataFrame
    # append to the existing CSV without rewriting headers or index numbers
    #df_new.to_csv('data.csv', mode='a', index=False, header=False)

    


# df.at[0, 'Item Name'] = 'chicken'
# df.at[0, 'Quantity'] = 2
# df.at[0, 'Expiration Date'] = '111626'
# print(df)