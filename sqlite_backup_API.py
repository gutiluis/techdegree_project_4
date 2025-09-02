import logging
import sqlite3

logging.basicConfig(level=logging.INFO)


logging.debug("""
loading and saving in-memory db
or 
online backup of a running db
""")

def make_backup(status, remaining, total):
    """
    works even if the db is being accesses by other clients or concurrently by the same connection
    """
    print(f"Copied {total-remaining} of {total} pages...")
main_db = sqlite3.connect("inventory.db")
target_db = sqlite3.connect("backup.db")
with target_db:
    main_db.backup(target_db, pages=1, progress=progress)
target_db.close()
main_db.close()
