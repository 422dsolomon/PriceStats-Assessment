import sqlite3
import pathlib
import os
import requests
from bs4 import BeautifulSoup as bs
import QueryAndCSV

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
        c.execute("DROP TABLE IF EXISTS Product_Pricing_Data")
        c.execute(create_table_sql)
    except:
        print(f"Error cannot create table")
        os.sys.exit(1)

def findPageNumber(url):
    r = requests.get(url).text
    soup = bs(r, 'html.parser')
    page_numbers = soup.find('ul', class_ = "page-list clearfix text-xs-center")
    page_num = page_numbers.find_all('li')
    total_pages = 0
    for page in page_num:    
        num = page.find('a', href = True)
        total_pages = max(total_pages, int(num['href'][-1]))
    return total_pages

def scrapeProducts(page):
    website = f"https://glacial.com.uy/8-vegetales?page={page}"
    r = requests.get(website).text
    soup = bs(r, 'html.parser')
    products = soup.find_all('div', class_ = "product-container")
    productsList = []
    for product in products:
        #Base Information
        product_id = None
        name = None
        desc = None
        reg_price = None
        sale_price = None
        OOSI = None
        url = None
        #Product name and link
        prod_name_and_link = product.find('h5', class_ = "product-title")
        name = prod_name_and_link.text
        link = prod_name_and_link.find('a', href = True)
        url = link['href']
        #Product description
        product_desc = product.find('div', class_ = "product-description-short")
        desc = product_desc.text
        #Out of stock index
        avialability_status = product.find('link')
        avilability = avialability_status['href'][19:]
        if avilability[0] == "I":
            OOSI = "True"
        else:
            OOSI = "False"
        #Product regular price and sales price
        prod_price = product.find('span')
        reg_price = prod_price.get('content')
        if not reg_price:
            prod_price = product.find('span', class_ = "regular-price")
            reg_price = prod_price.text[2:]
            sale = product.find('span', class_ = 'price')
            sale_price = sale.get('content')
        #Output
        productList = [product_id,name,desc,reg_price,sale_price,OOSI,url]
        productsList.append(productList)

    return productsList

def main():
    #Database Path
    db_path = "./PriceStats Technical Assessment/prod_sqlite.db"

    #Website URL
    url = "https://glacial.com.uy/8-vegetales"

    #Connect to the Database 
    conn = sqlConnect(db_path)

    #Instantiate cursor
    db_cursor = conn.cursor()

    #Create Table
    #Table Fields: Unique product identifier, Product name, Product description (when available), 
    # Price, Sale price (when available), Out of stock indicator (when available), 
    # URL the product was captured from
    sql_create_table = """CREATE TABLE IF NOT EXISTS Product_Pricing_Data (product_id interger, 
                            product_name text, product_desc text, reg_price interger, 
                            sale_price interger, OOSI text, URL text);"""
    
    if conn is not None:
        create_table(conn, sql_create_table)
    
    #Get number of pages
    total_pages = findPageNumber(url)
    totalProductsList = []

    #WebScrape
    for i in range(1, total_pages+1):
        productsList = scrapeProducts(i)
        totalProductsList.append(productsList)

    #Insert data into SQLite
    sql = """INSERT INTO Product_Pricing_Data(product_id,product_name,product_desc,reg_price,sale_price,OOSI,URL)
                VALUES(?,?,?,?,?,?,?)"""
    
    for productPage in totalProductsList:
        for products in productPage:
            db_cursor.execute(sql, products)

    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    main()
    QueryAndCSV

