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
        print("Enter the category this item belongs to:\n")
        print("\n- Dairy (ex. cheese, Eggs)\n")
        print("- Fresh Produce(ex. fruit, veggies)")
        print("- Protein (ex. chicken, fish ,shell fish )")
        print("- Condiments (ex. mayo,relish)")
        print("- Drinks (ex. juices, tea, water , smoothie)")

        category = input("-Dairy(ex. cheese, Eggs)\n").lower()

        quantity = int(input("Enter the number of units of this item: "))
        expDate = input("Enter the expiration date in the following format (MM/DD/YYYY): ")
        dateAdded = datetime.now()

        # parse expiration date to datetime object
        parsedDate = datetime.strptime(expDate, "%m/%d/%Y")

        # create a dictionary for each food entry
        newRow = {
            "Item Name": items,
            "Quantity": quantity,
            "Expiration Date": parsedDate,
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

    # find rows with that item name
    # .str.strip() takes away whitespace
    matches = (
        df["Item Name"].str.strip().str.lower() == itemName.strip().lower()
    )

    # finds the index of the match(es)
    matchingRows = df.index[matches]

    if matchingRows.empty:
        print(itemName, " was not found in your inventory.")
        return # user should be rerouted to the main menu

    # if there is more than match, user must select which one
    if len(matchingRows) > 1:
        print("Which entry for ", itemName, " do you want to update?")

        for number, rowIndex in enumerate(matchingRows, start=1):
            expiration = df.loc[rowIndex, "Expiration Date"]
            added = df.loc[rowIndex, "Date Added"] # targets that exact cell
            print(number, " Expires: ", expiration, " | Added:", added)

        try:
            choice = int(input("Enter the entry number: "))
        except ValueError:
            print("Try again. Enter a whole number.")
            return

        # checks if entry is within range of choice list
        if not 1 <= choice <= len(matchingRows):
            print("That number choice is out of range.")
            return

        # index of row the user wants to update
        rowIndex = matchingRows[choice - 1]
    else:
        rowIndex = matchingRows[0]

    newDate = input("Enter the new expiration date in the following format (MM/DD/YYYY)").strip()

    try:
        # parse expiration date to datetime object
        parsedDate = datetime.strptime(newDate, "%m/%d/%Y")
    except ValueError:
        print("Enter a valid date in MM/DD/YYYY format.")
        return

    df.loc[rowIndex, "Expiration Date"] = parsedDate.isoformat()
    df.to_csv(INVENTORY_FILE, index=False)

    print("Expiration date updated successfully.")
    print(loadInventory())



    
def main():
    # createList()
    updateExpDate("chicken")
    # print(loadInventory())

main()