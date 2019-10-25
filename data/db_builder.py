#===========================================================

#db_builder is to be used to create the database and tables.

#===========================================================

import sqlite3

db = sqlite3.connect("spew.db") #open if file exists, otherwise create
c = db.cursor()                 #facilitate db ops

#======================================================================

c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, password TEXT);") #create table for user login credentials
c.execute("CREATE TABLE IF NOT EXISTS blogs(blog_id INTEGER PRIMARY KEY AUTOINCREMENT, blog_name TEXT UNIQUE, blog_author_id INTEGER, blog_last_update timestamp, FOREIGN KEY(blog_author_id) REFERENCES users(id));")
c.execute("CREATE TABLE IF NOT EXISTS entries(entry_id INTEGER PRIMARY KEY AUTOINCREMENT, entry_blog INTEGER, entry_title TEXT, entry_content TEXT, entry_date timestamp, entry_last_update timestamp, FOREIGN KEY(entry_blog) REFERENCES blogs(blog_id));")

#=========================================================================================================================================

db.commit() #save changes
db.close()  #close database
