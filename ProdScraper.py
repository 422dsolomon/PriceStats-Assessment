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
    