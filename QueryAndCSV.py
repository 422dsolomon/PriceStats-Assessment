import pandas as pd
import sqlite3
from ProdScraper import sqlConnect

#Database Path
db_path = "./prod_sqlite.db"

#Connect to database
conn = sqlConnect(db_path)

#Instantiate cursor
db_cursor = conn.cursor()

# Order
db_cursor.execute("""SELECT * FROM Product_Pricing_Data ORDER BY COALESCE(reg_price, sale_price) DESC, product_name""")

#Commit
conn.commit()

#print out CSV
for i in db_cursor:
    print(i)

#Close
conn.close()