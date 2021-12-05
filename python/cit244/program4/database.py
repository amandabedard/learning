"""
Book Store Database
Amanda Bedard
December 3, 2021

This program creates and runs a database for a bookstore.
It performs different operations on the tables.
"""
# Importing sqlite for database actions and csv for reading the files
import sqlite3
import csv

"""
    This function will create the connection to the database and
    determine if initialization was successful
    Returns: the database object created or 'None'
"""
def connectToDB():
    dbName='program4.db'
    # Surrounding in try catch to ensure successful initialization
    try: 
      database = sqlite3.connect(dbName)
      # We have a bad connection. Throw an error and escape the function
      if not database:
          print('Bad connection')
          raise Exception()

      # No exception was raised, we will keep going
      print('Connected to DB. Setting up tables.')
      # Creating the tables now with our connection
      createTables(database)
      print('Created tables.')
    except:
        # Something went wrong, we are not going to be using our database this time
        print('Error creating DB')
        return None
    # No errors happened in the try, our initialization was a success!
    print('DB initialization successful.')
    return database

"""
    This function creates the tables in the database if necessary
"""
def createTables(database):
    # Create table statements for each of the tables we need
    createCustomersSQL="""CREATE TABLE IF NOT EXISTS customers (
	custID integer PRIMARY KEY,
	name text NOT NULL,
	address text NOT NULL,
	age integer NOT NULL,
	income decimal NOT NULL,
	loginId text NOT NULL,
	password text NOT NULL
    );
    """
    createPublishersSQL="""CREATE TABLE IF NOT EXISTS publishers (
	publisherID integer PRIMARY KEY,
	name text NOT NULL,
	address text NOT NULL,
	discount integer
    );
    """
    createBooksSQL="""CREATE TABLE IF NOT EXISTS books (
	isbn text PRIMARY KEY,
	title text NOT NULL,
	author text NOT NULL,
	qtyInStock integer NOT NULL,
	price decimal NOT NULL,
	cost decimal NOT NULL,
	year integer NOT NULL,
    publisherID integer NOT NULL,
	FOREIGN KEY (publisherID) REFERENCES publishers (publisherID)
    );
    """
    createOrdersSQL="""CREATE TABLE IF NOT EXISTS orders (
	orderNum integer PRIMARY KEY,
    custID integer NOT NULL,
	cardnum text NOT NULL,
	cardMonth integer NOT NULL,
	cardYear integer NOT NULL,
	orderDate date NOT NULL,
	shipDate date NOT NULL,
	FOREIGN KEY (custID) REFERENCES customers (custID)
    );
    """
    createOrderListSql="""CREATE TABLE IF NOT EXISTS orderList (
	orderNum integer NOT NULL,
	isbn text NOT NULL,
	quantity integer NOT NULL,
    PRIMARY KEY (orderNum, isbn),
	FOREIGN KEY (orderNum) REFERENCES orders (orderNum)
    FOREIGN KEY (isbn) REFERENCES books (isbn)
    );
    """
    sqlList = [createPublishersSQL, createBooksSQL, createCustomersSQL, createOrdersSQL, createOrderListSql]

    # We will run through all the tables we need to create and make them
    for statement in sqlList:
        dbCursor = database.cursor()
        dbCursor.execute(statement)

"""
    This function reads the text from a user specified file, for a specific, existing table
"""
def readTextFile(tableName, fileName, database):
    data = []
    # We are opening the csv with the ' specified as quote so we do not read the commas from the sample data
    with open(fileName, encoding="utf-8") as dataFile:
        rows = csv.reader(dataFile, skipinitialspace=True, quotechar="'")
        # Appending the data to the empty list
        for row in rows:
            data.append(row)
    dbCursor = database.cursor()
    # Since each of the tables has different keys, we will need different queries
    queryDict = {
        'customers': "INSERT INTO customers (custID, name, address, age, income, loginId, password) VALUES (?, ?, ?, ?, ?, ?, ?);",
        'books': "INSERT INTO books (isbn, title, author, qtyInStock, price, cost, year, publisherID) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
        'publishers': "INSERT INTO publishers (publisherID, name, address, discount) VALUES (?, ?, ?, ?);",
        'orders': "INSERT INTO orders (orderNum, custID, cardnum, cardMonth, cardYear, orderDate, shipDate) VALUES (?, ?, ?, ?, ?, ?, ?);",
        'orderList': "INSERT INTO orderList (orderNum, isbn, quantity) VALUES (?, ?, ?);"
    }
    # If we have a table that exists, run the correct query and commit to the database
    if tableName in queryDict.keys():
        query = queryDict.get(tableName)
        dbCursor.executemany(query, data)
        database.commit()

"""
    This function displays all the values in a user specified valid table
"""
def displayAll(displayKey, database):
    # Display all the rows for a specified table with a SELECT * query
    dbCursor = database.cursor()
    dbCursor.execute('SELECT * FROM %s;' % displayKey)
    rows = dbCursor.fetchall()
    print('\nAll data for table %s:\n' % displayKey)
    for row in rows:
        print(row)

"""
    This function joins four different tables to give a report on data from the orderList table
"""
def reportOnData(database):
    dbCursor = database.cursor()
    # Here we have the query that gathers the data specified and joins the tables
    # on the foreign keys
    orderListQuery = """SELECT
    orders.custID,
    customers.name,
    customers.address,
    books.title,
    books.author,
    publishers.name
    FROM orderList
    LEFT JOIN orders ON orders.orderNum = orderList.orderNum
    LEFT JOIN customers ON customers.custID = orders.custID
    LEFT JOIN books ON books.isbn = orderList.isbn
    LEFT JOIN publishers ON books.publisherID = publishers.publisherID
    """
    dbCursor.execute(orderListQuery)
    rows = dbCursor.fetchall()
    # Printing the details after we query
    print('Order Details:')
    for row in rows:
        print(row)

"""
    The main function.
    This function creates the initial connection to the database
    If successful, it provides the user a list of actions that can be performed
    If necessary, it will validate the data before calling a function
"""    
def main():
    # A boolean to keep the loop alive, a dict for the tables we can read from, and our db connection
    activeDb = True
    printAllDict = {'1':'customers', '2':'publishers', '3':'books'}
    database = connectToDB()

    # We are looping if we were successful with our initialization
    while activeDb and database != None:
        print('\nOptions are as follows:')
        print('1 - read from text files')
        print('2 - display all data')
        print('3 - report on orders')
        choice = input('Any other value will quit: ')
        if choice == '1':
            # Reading from our text files
            tablename = input('What is the table you wish to load into: ')
            filename = input('What is the name of the file: ')
            readTextFile(tablename, filename, database)

        elif choice == '2':
            # Which value would we like to display?
            print('\nDisplay options are as follows:')
            print('1 - customers')
            print('2 - publishers')
            print('3 - books')
            display = input('Any other value will return to menu: ')
            if display in printAllDict.keys():
              displayAll(printAllDict.get(display), database)

        elif choice == '3':
            # Let's get a report on the order list items by providing details
            reportOnData(database)
        else:
            # User did not pick an action, we will end execution
            print('Closing connection and exiting program')
            database.close()
            activeDb = False

main()