# I want to store the data using classes and file handling
# create different files to store for different lists

import pandas as pd
from datetime import datetime
from pathlib import Path

INVENTORY_FILE = Path(__file__).resolve().parent / "inventory-list.csv"
COLUMNS = ["Item Name", "Quantity", "Expiration Date", "Category", "Date Added"]

# retrieves inventory if list exists
# returns an empty table if it doesn't exist
def loadInventory():
    # returns the table empty
    if not INVENTORY_FILE.exists() or INVENTORY_FILE.stat().st_size == 0:
        return pd.DataFrame(columns=COLUMNS)

    return pd.read_csv(INVENTORY_FILE)

def saveItems(newRow):
    # if it doesn't exist, this variable returns False
    needHeaders = (not INVENTORY_FILE.exists() or INVENTORY_FILE.stat().st_size == 0)

    # converts to dataframe
    newItem = pd.DataFrame([newRow], columns=COLUMNS)
    # append to the existing CSV without rewriting headers or index numbers
    newItem.to_csv(INVENTORY_FILE, mode="a", index=False, header=needHeaders)


def createList():
    df = loadInventory()
    continueList = "Y"

    # checks if the fridge/inventory list is eempty
    if df.empty:
        print("Your Inventory is empty.")

    # while loop that allows user to continue to enter values until they are finished
    while continueList == "Y" :
        items = input("Enter the name of the item: ").lower()
        category = input("Enter the category this item belongs to (Dairy, Fresh Produce, Protein, Condiments, or Drinks):").lower()
        quantity = int(input("Enter the number of units of this item: "))
        expDate = input("Enter the expiration date in the following format (MM/DD/YYYY): ")
        dateAdded = datetime.now()

        # parse expiration date to datetime object
        parsedDate = datetime.strptime(expDate, "%m/%d/%Y")

        # create a dictionary for each food entry
        newRow = {
            "Item Name": items,
            "Quantity": quantity,
            "Expiration Date": expDate,
            "Category": category,
            "Date Added": dateAdded
        }

        # save item and load inventory
        saveItems(newRow)
        print("Item added successfully.\n")
        print(loadInventory())

        continueList = input("Would you like to enter another item? (Y/N): ").upper()

def updateExpDate(itemName):
    df = loadInventory()

    # checks if the fridge/inventory list is eempty
    if df.empty:
        print("Your Inventory is empty.")

    # get index using item's name index.get_loc()
    itemIndex = df.columns.get_loc('Item Name')
    # then .iloc() to locate the value
    value = df.iloc[[itemIndex]]
    print(value)

    # use value variable to locate exp date
    

    # df.loc['Item Name'][itemName]


    
def main():
    # createList()
    updateExpDate("chicken")

main()