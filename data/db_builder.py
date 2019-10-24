#===========================================================

#db_builder is to be used to create the database and tables.

#===========================================================

import sqlite3

db = sqlite3.connect("spew.db") #open if file exists, otherwise create
c = db.cursor()                 #facilitate db ops

#======================================================================

c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT);") #create table for user login credentials

#=========================================================================================================================================

db.commit() #save changes
db.close()  #close database
