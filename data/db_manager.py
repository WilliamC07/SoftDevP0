#========================================================================================

#db_manager is to be used to facilitate operations from frontend/backend to the database.

#========================================================================================

import sqlite3

def addLogin(inputName, inputPassword): #facilitate adding new login credentials
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    c.execute("SELECT * FROM users WHERE name = ?;" , inputName) #all instances of name in database
    if c.fetchone() is None: #if name is not found in database
        c.execute("INSERT INTO users(name, password) VALUES(?, ?);" , (inputName, inputPassword)) #add login credentials
        db.commit() #save changes
        db.close() #close database
        return ""
    else:
        db.commit() #save changes
        db.close() #close database
        return "Username exists!"

# addLogin("admin", "password") #test adding login credentials with new name
# addLogin("admin", "password") #test adding login credentials with existing name

def verifyLogin(inputName, inputPassword): #verify login credentials
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    c.execute("SELECT * FROM users WHERE name = ? AND password = ?;" , (inputName, inputPassword)) #any rows where the inputs match
    if c.fetchone() is not None: #if login credentials are found in database
        db.commit() #save changes
        db.close() #close database
        return ""
    else:
        db.commit() #save changes
        db.close() #close database
        return "Login credentials not found!"

# verifyLogin("admin", "password") #test existing login
# verifyLogin("admin", "fakePassword") #test fake login credentials
