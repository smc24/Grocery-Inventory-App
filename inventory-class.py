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
        parsedDate = datetime.strptime(expDate, "%m/%d/%Y").isoformat()

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

    def updateName(self):

        df = self.loadInventory()

        itemName = input("Enter the current food name: ").lower()

        matches = df.index[df["Item Name"].str.lower() == itemName].tolist()

        if not matches:
            print("Item not found.")
            return

        newName = input("Enter the new food name: ").lower()

        df.loc[matches, "Item Name"] = newName

        df.to_csv(self.INVENTORY_FILE, index=False)

        print("Food name updated successfully!")
        print(self.loadInventory())

    def updateQuantity(self):

        df = self.loadInventory()

        itemName = input("Enter the food name: ").lower()

        matches = df.index[df["Item Name"].str.lower() == itemName].tolist()

        if not matches:
            print("Item not found.")
            return

        print("Current quantity:", df.loc[matches[0], "Quantity"])

        newQuantity = int(input("Enter the new quantity: "))

        if newQuantity < 0:
            print("Quantity cannot be negative.")
            return

        df.loc[matches[0], "Quantity"] = newQuantity

        df.to_csv(self.INVENTORY_FILE, index=False)

        print("Quantity updated successfully!")
        print(self.loadInventory())

    def updateExpDate(self, itemName):
        df = self.loadInventory()

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
        df.to_csv(self.INVENTORY_FILE, index=False)

        print("Expiration date updated successfully.")
        print(self.loadInventory())

    def updateCategory(self, itemName):
        df = self.loadInventory()

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

        newCategory = input("Enter the new category for this item: ").strip()

        df.loc[rowIndex, "Category"] = newCategory
        df.to_csv(self.INVENTORY_FILE, index=False)

        print("Category updated successfully.")
        print(self.loadInventory())

    def removeItem(self):

        df = self.loadInventory()

        itemName = input("Enter the food name to remove: ").lower()

        matches = df.index[df["Item Name"].str.lower() == itemName].tolist()

        if not matches:
            print("Item not found.")
            return

        df = df.drop(matches[0]).reset_index(drop=True)

        df.to_csv(self.INVENTORY_FILE, index=False)

        print("Food item removed successfully!")
        print(self.loadInventory())

def main():
    # while loop that allows user to continue to enter values until they are finished
    continueList = "Y"

    while continueList == "Y" :
        try:   
            items = input("Enter the name of the item: ").lower()
            print("Enter the category this item belongs to:")
            print("- Dairy (ex. cheese, eggs)")
            print("- Fresh Produce (ex. fruit, veggies)")
            print("- Protein (ex. chicken, fish, shell fish)")
            print("- Condiments (ex. mayo, relish)")
            print("- Drinks (ex. juices, tea, water, smoothie)")

            category = input("Select a category: \n").lower()

            quantity = int(input("Enter the number of units of this item: "))
            expDate = input("Enter the expiration date in the following format (MM/DD/YYYY): ")
            dateAdded = datetime.now()
        except ValueError:
            print("Invalid input. Please enter the correct data types.")
            continue

        fridgeList = Inventory(items, quantity, expDate, category, dateAdded)
        fridgeList.createList(items, quantity, expDate, category, dateAdded)
        

        continueList = input("Would you like to enter another item? (Y/N): ").upper()

    # fridgeList.updateExpDate("cheese")
    # fridgeList.updateCategory("cheese")
    # fridgeList.updateName()
    # fridgeList.updateQuantity()
    fridgeList.removeItem()
    
        

main()