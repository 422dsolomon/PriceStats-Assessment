import sqlite3
import pathlib
import os
import requests
from bs4 import BeautifulSoup as bs

def sqlConnect(db_path):
    path_to_db = pathlib.Path(db_path).absolute().as_uri()
    connection = None
    try:
        connection = sqlite3.connect(f"{path_to_db}?mode=rw", uri = True)
    except:
        print(f"Error trying to open data base, please check that file exists: {path_to_db}")
        os.sys.exit(1)
    return connection

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except:
        print(f"Error cannot create table")
        os.sys.exit(1)


def main():
    #Database Path
    db_path = "./prod_sqlite.db"

    #Connect to the Database 
    conn = sqlConnect(db_path)

    #Instantiate cursor
    db_cursor = conn.cursor()

    #Create Table
    #Table Fields: Unique product identifier, Product name, Product description (when available), 
    # Price, Sale price (when available), Out of stock indicator (when available), 
    # URL the product was captured from
    sql_create_table = """CREATE TABLE IF NOT EXISTS Product_Pricing_Data (product_id interger, 
                            product_name text, product_desc text, price interger, 
                            sale_price interger, OOSI boolean, URL text);"""
    
    if conn is not None:
        create_table(conn, sql_create_table)
    else:
        print("Error! cannot create the database connection")

    
    if __name__ == "__main__":
        main()

