from contextlib import ExitStack
import csv
import logging
import sqlite3



logging.basicConfig(level=logging.INFO)



logging.debug("turn a sqlite.db to a csv file")
def make_csv_backup_from_sqlite(db_path, csv_path, table_name="products"):
    logging.debug("""
                  exitstack object that closes automatically
                  same as wiritng multiple with statments""")
    with ExitStack() as stack:
        
        logging.debug("""
                      enter_context is a method from exitstack
                      context manager: __entet__, __exit__
                      opens a connection to the sqlite db
                      stack.enter_context() registers the connection so that it will automatically be closesd when the block ends
                      equivalent to with sqlite3.connect(db_path) as conn
                      """)
        conn = stack.enter_context(sqlite3.connect(db_path))
    
        
        logging.debug("""
                      context manager: __enter__, __exit__
                      opens the output csv file in write mode.
                      newline='' ensures correct line endings on al OS
                      registered with the stack""")
        f = stack.enter_context(open(csv_path, "w", newline=""))

        logging.debug(""""
                      not a context manager: __enter__, __exit__
                      create cursor object""")
        cursor = conn.cursor()

        logging.debug("contextlib close exitstack")
        stack.callback(cursor.close)

        logging.debug("query all rows")
        cursor.execute(f"SELECT * FROM {table_name}")
        
        logging.debug("query everything and write a python list of tuples [('ex', 1, 2)] ")
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        
        logging.debug("object knows how to write rows in the csv file.")
        writer = csv.writer(f)
        
        logging.debug("writes the first row in the csv file")
        writer.writerow(headers)
        writer.writerows(rows)
        
    logging.info("csv backup file finished...")