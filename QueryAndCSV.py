import pandas as pd
import sqlite3
from ProdScraper import sqlConnect

#Database Path
db_path = "./PriceStats Technical Assessment/prod_sqlite.db"

#Connect to database
conn = sqlConnect(db_path)

#Instantiate cursor
db_cursor = conn.cursor()

db_cursor.execute("""SELECT * FROM Product_Pricing_Data ORDER BY COALESCE(reg_price, sale_price), product_name""")

conn.commit()

# db_file = "./PriceStats Technical Assessment/prod_sqlite.db"

# conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_COLNAMES)
# db_df = pd.read_sql_query("SELECT * FROM Product_Pricing_Data", conn)

# db_df.to_csv('database2.csv', index=False)

conn.close()