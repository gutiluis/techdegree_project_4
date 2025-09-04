#!/bin/python
from models import (Base, session,
                    Product, engine)
from sqlite_CSV_backup import *
from datetime import datetime
import csv
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

logging.debug("app function has a clean_id wrapper/helper function")
def clean_id(id_string, options):
    try:
        product_id = int(id_string)
    except ValueError:
        input("""
              \n****** ID ERROR ******
              \rThe id should be a number without a symbol...
              \rEx: 1, 2, 3...
              \rPress Enter to return to the last menu... 
              \r**********************""")
        logging.debug("the return will return None... affecting the while loop")
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f"""
              \n****** ID ERROR ******
              \rOptions: {options}"
              \rPress Enter to return to the last menu... 
              \r**********************""")
            return


logging.info("cleaning price column string data type from csv. remove $ and make integer.")
def clean_price(price_string_csv):
    while True:
        try:
            replace_m = price_string_csv.replace("$", "").strip()
            price_float = float(replace_m)
            return int(price_float * 100)
        except ValueError:
            price_string_csv = input("""
              \n***** PRICE ERROR *****
              \rThe price should be a number without a currency symbol...
              \rEx: 12.99
              \rTry again: """)
        

def clean_quantity(quantity_string):
    while True:
        try:
            quantity_string = quantity_string.strip().replace(",", ".")
            return float(quantity_string)
        except ValueError:
            quantity_string = input("""
              \n****** QUANTITY ERROR ********
              \rThe quantity should be a number without symbols
              \rEx: 1, 200
              \rTry again: """)


logging.info("csv format: 2/3/2000. The parameter in the function can be anything.")
def clean_date(date_string_csv):
    while True:
        try:
            dt = datetime.strptime(date_string_csv, "%m/%d/%Y").date()
            return dt
        except ValueError:
            date_string_csv = input("""
              \n***** DATE ERROR *****
              \rThe date format should be MM/DD/YYYY.
              \rEx: 01/12/2003
              \rTry again: """)


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
                quantity = clean_quantity(row["product_quantity"])
                date = clean_date(row["date_updated"])
                new_product = Product(
                    product_name=name, 
                    product_price=price, 
                    product_quantity=quantity, 
                    date_updated=date
                )
                session.add(new_product)
        session.commit()


logging.info("app function")
def app():
    app_running = True
    while app_running:
        user_interaction = selections_menu()

        if user_interaction == "v":
            """
            logging.debug("getting and displaying a product. by id.")
            for product in session.query(Product):
                print(f"{product.product_id} | {product.product_name}")
            input("\nPress enter and return to main menu...")
            """
            logging.debug("grab length of db and use as a range?")
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                id_choice = input(f"""
                      \nId Options: {id_options}...
                      \rProduct id: """)
                logging.debug("clean_id() has 2 parameters too")
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(Product.product_id==id_choice).first()
            logging.debug("""product price get back to an actual price and not the price and cents
                          ex: 10.99 instead of 1,099""")
            print(f"""
                  \nProduct name: {the_product.product_name}
                  \rProduct current price: ${the_product.product_price / 100}
                  \rProduct quantity - (YYYY-MM-DD): {the_product.date_updated}""")
            input("\nPress enter to return to the main menu()...")
            
        elif user_interaction == "a":
            product_name = input("Product name: ").strip()

            product_price = clean_price(input("Product price (Ex: 25.64): "))
            product_quantity = clean_quantity(input("Product quantity: "))
            date_updated = clean_date(input("Date updated (Ex: 11/1/2018): "))
            
            logging.debug("create and add product session to db.")
            new_product = Product(
                product_name=product_name,
                product_price=product_price,
                product_quantity=product_quantity,
                date_updated=date_updated
            )
            session.add(new_product)
            session.commit()
            print(f"\nProduct '{product_name}' added successfully!\n")
            time.sleep(1)
            
        elif user_interaction == "b":
            make_csv_backup_from_sqlite("inventory.db", "backup_csv.csv")
            logging.info("CSV db backup created...")

        else:  # user_interaction == "e"
            print("\nGOODBYE")
            app_running = False


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv_to_db()
    app()
