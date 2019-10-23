#====================================================================================================

#db_builder is to be used to create the database and tables.

#====================================================================================================

import sqlite3

db = sqlite3.connect("spew.db") #open if file exists, otherwise create
c = db.cursor()                 #facilitate db ops

#====================================================================================================

c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT);") #create table for user login credentials

c.execute("INSERT INTO users(name, password) VALUES('admin', 'password');") #add admin login

#====================================================================================================

db.commit() #save changes
db.close()  #close database

#====================================================================================================