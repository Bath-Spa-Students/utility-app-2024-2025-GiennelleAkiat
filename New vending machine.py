import glob
import json
import random
data_path = "data for vending machine/"
products_list = list()
products_list.append({
    "ID": 0,
    "Stock Num": 0,
    "Item Name": "-----",
    "Price": 0,
    })
product_id = 0

#===============================================================
#---------------------FUNCTIONS
#===============================================================

#-------------------Save Data
def save_data(type,item_name,stock):
    json_file = f"{data_path}{type.lower()}.json"
    with open(json_file,"r") as file:
         json_data = json.load(file)
    item_data = json_data["Items"][item_name]
    item_data["Stock"] = stock
    with open(json_file,"w") as file:
         file.write(json.dumps(json_data,indent= 3))

#-------------------Load Data
def load_data(type):
    json_file = f"{data_path}{type.lower()}.json"
    with open(json_file,"r") as file:
         json_data = json.load(file)
    return json_data

#-------------------Sum of all purchases
def sumitems(customer_items):
    sumitems = 0
    for item_name,item_data in customer_items.items():
        sumitems += item_data['Price']
    return sumitems

#-------------------Customer Budget
def change(customer_items, money):
    money_spent = money
    while money_spent > 0:
        for item_name,item_data in customer_items.items():
            money_spent -= item_data['Price']
        return money_spent
    
#-------------------Check type
def check_type(customer_items):
    type_list = []
    pair_list = set()
    for item_name,item_data in customer_items.items():
        if item_data['Type'] not in type_list:
            type_list.append(item_data['Type'])
    for item_name,item_data in customer_items.items():
        if item_data["Pair"] not in type_list:
            pair_list.add(item_data["Pair"])

    return pair_list

#-------------------Show recommended
def show_rec(customer_items,money):
    item_pairs = check_type(customer_items)
    for type in item_pairs:
        item_data = load_data(type)
        items_keys = list(item_data["Items"].keys())
        random.shuffle(items_keys)
        random_item = items_keys[0]
        random_item_price = item_data["Items"][random_item]["Price"]
        pair=""
        type_name=""
        name=""
        # print(json.dumps(customer_items, indent=4))
        for item_name,item_data in customer_items.items():
            name = item_name
            if item_data["Pair"] in type:
                pair=item_data["Pair"]
                type_name=item_data["Type"]
                break
        print(f"Would you like to add {random_item} with your {name} for ${random_item_price}?")
        y_or_n = input("Y/N: ")
        y_or_n = y_or_n.lower()
        if y_or_n == "y":
            if random_item not in customer_items:
                customer_items[random_item]={
                    "Count":1,
                    "Price":random_item_price,
                    "Type": pair,
                    "Pair":type_name
                }
            else:
                customer_items[random_item]["Count"] += 1
            #--- Print items dispensed
            print("")
            for item_name,item_data in customer_items.items():
                print(f"Item {item_name} has been dispensed.")
            
            #--- Print amount of money user has left
            print(f"Money left: ${change(customer_items, money)}", end="\n ------- \n")

            #--- If user has no money
            while int(change(customer_items, money)) < 0:
                user_input=input("[NOT ENOUGH MONEY] \n Want to add more money? Y/N ").lower()
                if user_input == "y":
                    money += int(input("Enter amount of money to add: "))
                else:
                    print("U BROKE GET OUT!!!!!")
                    break
                   
#-------------------Printing the Receipt
def final_bill(customer_items,receipt, money):
    for item_name,item_data in customer_items.items():
        #Print all items and prices
        receipt += f"\n{item_name} \t --------------  ${item_data['Price']}"
    #Print total items and sum
    receipt += f"\n\nNO. OF ITEMS: | {len(customer_items.keys())} \nTOTAL: | ${sumitems(customer_items)} \nPAID: | ${money} \nCHANGE: | ${change(customer_items, money)}"
    return receipt

#-------------------The Vending Machine Process
def vending_machine(products_list, done, customer_items, money):
    while not done:
        try:
            purchases = int(input("Enter item ID: "))

            #--- Operation to continue if user inputs wrong id
            if purchases > total_products or purchases < 0:
                print("[INVALID ITEM ID | TRY AGAIN]")
            #--- Keep appending customer purchases to the item list
            elif purchases != 0:
                product_data = products_list[purchases] 
                item_name = product_data["Item Name"]
                num_item = customer_items.get(item_name, {}).get("Count", 0)
                num_item += 1
                customer_items[item_name] = {
                    "Count":num_item,
                    "Price":product_data["Price"],
                    "Type": product_data["Type"],
                    "Pair":product_data['Pair']
                }
            
            #--- If user finally inputs "0"
            else:
                done = True
            
            #--- Print items dispensed
            print("")
            for item_name,item_data in customer_items.items():
                print(f"Item {item_name} has been dispensed.")
            
            #--- Print amount of money user has left
            print(f"Money left: ${change(customer_items, money)}", end="\n ------- \n")

            #--- If user has no money
            if int(change(customer_items, money)) < 0:
                user_input=input("[NOT ENOUGH MONEY] \n Want to add more money? Y/N ").lower()
                if user_input == "y":
                    money += int(input("Enter amount of money to add: "))
                else:
                    print("U BROKE GET OUT!!!!!")
                    done = True
            
            #--- Print bill if done
            if done:
                show_rec(customer_items,money)
                print(final_bill(customer_items, receipt, money))
                
                 
        #In case user inputs smth other than an integer
        except ValueError:
            print("[INVALID ITEM ID | TRY AGAIN]")

#===============================================================
#---------------------VENDING MACHINE ITEMS
#===============================================================

for file in glob.glob(f"{data_path}*.json"):
    with open(file,"r") as jsonFile:
            json_data= json.load(jsonFile)
    for item_name, item_data in json_data["Items"].items():
        product_id += 1
        # print(item_name,data["Stock"])
        products_list.append({
             "ID" : product_id,
             "Stock Num": item_data["Stock"],
             "Item Name": item_name,
             "Price": item_data["Price"],
             "Type": json_data["Type"],
             "Pair": json_data["Pair"]
        })


#===============================================================
#---------------------PRINTING ITEMS
#===============================================================
print("""
===============================================================
-------------------VENDING MACHINE ITEMS-----------------------
===============================================================""")
print("ID".ljust(4), "ITEM".ljust(14), "COST".rjust(7), "NO. IN STOCK".ljust(5), sep=" | ")
print("-" * 52)


#------------------------PRINTING ITEMS
for i in products_list:
    print(f"{i['ID']:<4} {i['Item Name']:<14} | ${i['Price']:>7.2f} | {i['Stock Num']:<5}")

#------------------------PRINTING INTRUCTIONS

print("""
-----------------
ENTER THE ITEM ID YOU WISH TO PURCHASE
TYPE '0' IF DONE
-----------------
""")

#===============================================================
#---------------------CUSTOMER INPUT
#===============================================================

#---- List of Items Customer will buy
customer_items = dict()
done = False
total_products = len(products_list)-1
money = int(input("Enter amount of money you have: "))

receipt = """\n\t-----------------\nPRODUCT \t| \t COST"""

#---- VENDING MACHINE PROCESS
vending_machine(products_list, done, customer_items, money)