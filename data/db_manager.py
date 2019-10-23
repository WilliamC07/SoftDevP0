#====================================================================================================

#db_manager is to be used to facilitate operations from frontend/backend to the database.

#====================================================================================================

import sqlite3

#====================================================================================================

db = sqlite3.connect("spew.db") #open file
c = db.cursor() #facilitate db ops

def dbCommitAndClose():
    db.commit() #save changes
    db.close() #close database

#====================================================================================================

def addLogin(inputName, inputPassword): #facilitate adding new login credentials
    c.execute("SELECT * FROM users WHERE name = '%s';" % inputName) #all instances of name in database
    if c.fetchone() is None: #if name is not found in database
        c.execute("INSERT INTO users(name, password) VALUES('%s', '%s');" % (inputName, inputPassword)) #add login credentials
        dbCommitAndClose()
        return "Successfully added login credentials!"
    else: 
        dbCommitAndClose()
        return "Username exists!"

print(addLogin("newAdmin", "newPassword")) #test adding login credentials with new name
#print(addLogin("admin", "password")) #test adding login credentials with existing name

#====================================================================================================

def verifyLogin(inputName, inputPassword): #verify login credentials
    c.execute("SELECT * FROM users WHERE name = '%s' AND password = '%s';" % (inputName, inputPassword)) #any rows where the inputs match
    if c.fetchone() is not None: #if login credentials are found in database
        dbCommitAndClose()
        return "Login credentials verified!"
    else: 
        dbCommitAndClose()
        return "Login credentials not found!"

#print(verifyLogin("admin", "password")) #test existing login
#print(verifyLogin("admin", "fakePassword")) #test fake login credentials

#====================================================================================================