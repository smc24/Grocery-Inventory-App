import pandas as pd
from datetime import datetime
from pathlib import Path

class Inventory:

    INVENTORY_FILE = Path(__file__).resolve().parent / "inventory-list.csv"
    COLUMNS = ["Item Name", "Quantity", "Expiration Date", "Category", "Date Added"]

    def __init__(self, itemName, quantity, expDate, category, dateAdded):
        self.itemName = itemName
        self.quantity = quantity
        self.expDate = expDate
        self.category = category
        self.dateAdded = dateAdded

    def loadInventory(self):
        # returns the table empty
        if not self.INVENTORY_FILE.exists() or self.INVENTORY_FILE.stat().st_size == 0:
            return pd.DataFrame(columns=self.COLUMNS)

        return pd.read_csv(self.INVENTORY_FILE)

    def saveItems(self, newRow):
        # if it doesn't exist, this variable returns False
        needHeaders = (not self.INVENTORY_FILE.exists() or self.INVENTORY_FILE.stat().st_size == 0)

        # converts to dataframe
        newItem = pd.DataFrame([newRow], columns=self.COLUMNS)
        # append to the existing CSV without rewriting headers or index numbers
        newItem.to_csv(self.INVENTORY_FILE, mode="a", index=False, header=needHeaders)

    def createList(self, itemName, quantity, expDate, category, dateAdded):
        df = self.loadInventory()

        # checks if the fridge/inventory list is eempty
        if df.empty:
            print("Your Inventory is empty.")

        # parse expiration date to datetime object
        parsedDate = datetime.strptime(expDate, "%m/%d/%Y")

        # create a dictionary for each food entry
        newRow = {
            "Item Name": itemName,
            "Quantity": quantity,
            "Expiration Date": parsedDate,
            "Category": category,
            "Date Added": dateAdded
        }

        # save item and load inventory
        self.saveItems(newRow)
        print("Item added successfully.\n")
        print(self.loadInventory())

        


def main():
    # while loop that allows user to continue to enter values until they are finished
    continueList = "Y"

    while continueList == "Y" :

        items = input("Enter the name of the item: ").lower()
        print("Enter the category this item belongs to:\n")
        print("- Dairy (ex. cheese, Eggs)")
        print("- Fresh Produce(ex. fruit, veggies)")
        print("- Protein (ex. chicken, fish ,shell fish )")
        print("- Condiments (ex. mayo,relish)")
        print("- Drinks (ex. juices, tea, water , smoothie)")

        category = input("Select a category: \n").lower()

        quantity = int(input("Enter the number of units of this item: "))
        expDate = input("Enter the expiration date in the following format (MM/DD/YYYY): ")
        dateAdded = datetime.now()

        fridgeList = Inventory(items, quantity, expDate, category, dateAdded)
        fridgeList.createList(items, quantity, expDate, category, dateAdded)
        

        continueList = input("Would you like to enter another item? (Y/N): ").upper()
        

main()