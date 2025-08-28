#!/bin/python
from models import (Base, session,
                    Product, engine)
import csv
from datetime import datetime
import logging
import sys
import time

logging.basicConfig(level=logging.INFO)
           

logging.info("create a menu to make selections.")
def selections_menu():
    while True:
        print("""
              \n
              \n## STORE INVENTORY ##
              \rSelect an option from the following letters:
              \rv) Enter v to view details of a single product by id.
              \ra) Enter a to add a new product.
              \rb) Enter b to make a backup of the database and export a new csv as backup.csv.
              \re) Press e to exit.""")
        user_interaction = input("Select v, a, b or e: ").lower().strip()
        if user_interaction in ["v", "a", "b", "e"]:
            return user_interaction
        else:
            input("Wrong selection. Return to the main menu by pressing enter. Then enter only v, a, b or e: ")

logging.info("cleaning csv date from csv file. The parameter in the function can be anything.")
def clean_date(date_string_csv):
    dt = datetime.strptime(date_string_csv, "%m/%d/%Y")
    return dt.date()

logging.info("cleaning price column from csv. remove $ and make integer.")
def clean_price(price_string_csv):
    replace_m = price_string_csv.replace("$", "").strip()
    price_float = float(replace_m)
    return int(price_float * 100)



logging.debug("6/6/2010")
logging.debug("$2.91")
logging.debug("product_name, product_price, product_quantity, date_updated")
logging.info("""function that will add the products
             \rlisted in the inventory.csv file to the db""")
def add_csv_to_db():
    with open("inventory.csv", newline="") as csvfile:
        iter_gener = csv.DictReader(csvfile, delimiter=",")  
        for row in iter_gener:
            logging.debug("""scalar value str() vs multiple values ORM""")
            no_dup_product_in_db = session.query(Product).filter(Product.product_name==row["product_name"]).one_or_none()
            if no_dup_product_in_db == None: # add product if no duplicate only
                name = row["product_name"]
                price = clean_price(row["product_price"])
                quantity = row["product_quantity"]
                date = clean_date(row["date_updated"])
                new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date)
                session.add(new_product)
        session.commit()
        
        #    model_instance_class = Product(
         #       product_name=row["product_name"],
          #      product_quantity=int(row["product_quantity"]),
           #     price=int(row["product_price"])
            #)
        #session.add(model_instance_class)
    #session.commit()


logging.info("app function")
def app():
    app_running = True
    while app_running:
        logging.info("First prompt the user should see.")
        user_interaction = selections_menu()
        if user_interaction == "v":
            logging.info("View product id.")
            pass
        elif user_interaction == "a":
            logging.info("Add a new product. ")
            product_name = input("Product name: ")
            product_price = input("Product price: ")
            product_quantity = input("Product quantity: ")
            date_updated = input("Date updated: ")
        
        elif user_interaction == "b":
            logging.info("Export csv to make a new db.")
            pass
        else:
            print("GOODBYE")
            logging.info("End of program. Turn off loop.")
            app_running = False



if __name__ == "__main__":
    Base.metadata.create_all(engine)
#    add_inventory_to_db()
    #app()
    add_csv_to_db()
 
    for product in session.query(Product):
        print(product)