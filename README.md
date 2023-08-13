# PriceStats-Assessment

Once downloaded files in terminal go into the folder with the files

## Download dependencies
Run: pip install -r requirements.txt

## Run Script
Run: python ProdScraper.py

## How the code works

### ProdScraper.py

1. sqlConnect(db_path)
Gets the uniform resource identifier(URI) of the database file. Then using the sqlite3 function connect() to connect to the database. If this is not happening it returns an error and closes the script
2. create_table(connection, SQL_Table)
Creates a cursor, deletes all the table if it exists, then using a SQLite format to create a new SQLite database. If there is an error it returns an error message and closes the script
3. findPageNumber(URL)
Using the requests python library, to get the information in text format. Then using BeautifulSoup python library to parse the HTML data. Using BeatifulSoup to find the number of pages. Get the total number of pages then returns that to be used to loop through the scrapeProducts function for all the pages
4. scrapeProducts(pages)
The input of pages allows to traverse the different pages of the website. Again start by using the requests library and the BeautifulSoup library to parse the HTML data. Looking into the div of the class product-container gives all the information that is needed. Start looping through the information of the products. During the loop, set each table value to a default value. By inspecting the website was able to find each HTML field that had the information that was needed. Once all the information was set to a variable, created a list of the information then added that to the output list. 
5. Main()
Instantiating database path, URL, using sqlConnect() function to connect to the database, instantiates the cursor, sets the table columns, creates the table with create_table() function, uses findPageNumber() function to get the the total number of pages that the scrapeProducts is going to run on. Creates an argument to add data to the sqlite database, then uses sqlite.execute to insert to data. then commit the data and close the connection. Calls QueryAndCSV to order and output csv.

### QueryAndCSV.py

Connects to database, instantiates a cursor reorders sql database using ORDER keyword. Used COALESCE to use regular price unless there is a sale price. Then uses the cursur to output information. Then lastly close the connection.
