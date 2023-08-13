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

def scrapeProducts(page):
    url = f"https://glacial.com.uy/8-vegetales?page={page}"
    r = requests.get(url).text
    soup = bs(r, 'html.parser')
    products = soup.find_all('div', class_ = "product-container")
    productsList = []
    for product in products:
        prod_name_and_link = product.find('h5', class_ = "product-title")
        link = prod_name_and_link.find('a', href = True)
        product_desc = product.find('div', class_ = "product-description-short")
        prod_price = product.find('span')
        name = prod_name_and_link.text
        price = prod_price.get('content')
        desc = product_desc.text
        url = link['href']
        productList = [None,name,desc,price,None,None,url]
        productsList.append(productList)

    return productsList

def main():
    #Database Path
    db_path = "./PriceStats Technical Assessment/prod_sqlite.db"

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
    
    #WebScrape
    productsList = scrapeProducts(1)

    #Insert data into SQLite
    sql = """INSERT INTO Product_Pricing_Data(product_id,product_name,product_desc,price,sale_price,OOSI,URL)
                VALUES(?,?,?,?,?,?,?)"""
    
    for product in productsList:
         db_cursor.execute(sql, product)

    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    main()

