#========================================================================================

#db_manager is to be used to facilitate operations from frontend/backend to the database.

#========================================================================================

import sqlite3

#========================================================================================

def addLogin(inputName, inputPassword): #facilitate adding new login credentials
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    c.execute("SELECT * FROM users WHERE name = '%s';" % inputName) #all instances of name in database
    if c.fetchone() is None: #if name is not found in database
        c.execute("INSERT INTO users(name, password) VALUES('%s', '%s');" % (inputName, inputPassword)) #add login credentials
        print("Successfully added login credentials!")
    else: 
        print("Username exists!")
    db.commit() #save changes
    db.close() #close database

# addLogin("newAdmin", "newPassword") #test adding login credentials with new name
# addLogin("admin", "password") #test adding login credentials with existing name

#===================================================================================

def verifyLogin(inputName, inputPassword): #verify login credentials
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    c.execute("SELECT * FROM users WHERE name = '%s' AND password = '%s';" % (inputName, inputPassword)) #any rows where the inputs match
    if c.fetchone() is not None: #if login credentials are found in database
        print("Login credentials verified!")
    else: 
        print("Login credentials not found!")
    db.commit() #save changes
    db.close() #close database

# verifyLogin("admin", "password") #test existing login
# verifyLogin("admin", "fakePassword") #test fake login credentials

#===================================================================
