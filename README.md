# PriceStats-Assessment

Once downloaded files in terminal go into the folder with the files

## Download dependencies
Run: pip install -r requirements.txt

## Run Script
Run: python ProdScraper.py

## How the code works

1. sqlConnect(db_path)
Gets the uniform resource identifier(URI) of the database file. Then using the sqlite3 function connect() to connect to the database. If this is not happening it returns an error and closes the script
2. create_table(connection, SQL_Table)
Creates a cursor, deletes all the table if it exists, then using a SQLite format to create a new SQLite database
3. findPageNumber(URL)

4. 
