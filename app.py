#!/bin/python
from models import (Base, session,
                    Product, engine)
import csv
import datetime
import logging
import sys
import time

logging.basicConfig(level=logging.INFO)

logging.info("""function that will add the products
             \rlisted in the inventory.csv file to the db""")
def add_inventory_to_db():
    with open("inventory.csv", newline="") as csvfile:
        iter_g = csv.DictReader(csvfile, delimiter=",")  
        for row in iter_g:
            model_instance_class = Product(
                product_name=row["product_name"],
                product_quantity=int(row["product_quantity"]),
                price=int(row["product_price"])
            )
        session.add(model_instance_class)
    session.commit()
           

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

logging.info("app function")
def app():
    app_running = True
    while app_running:
        logging.info("First prompt the user should see.")
        user_interaction = selections_menu()
        if user_interaction == "v":
            logging.info("View product id.")
            pass
            

if __name__ == "__main__":
    Base.metadata.create_all(engine)
#    add_inventory_to_db()
    selections_menu()