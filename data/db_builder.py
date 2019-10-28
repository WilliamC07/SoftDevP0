#===========================================================

#db_builder is to be used to create the database and tables.

#===========================================================

import sqlite3

db = sqlite3.connect("spew.db") #open if file exists, otherwise create
c = db.cursor()                 #facilitate db ops

#======================================================================

c.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT UNIQUE, user_password TEXT);") #create table for user login credentials
c.execute("CREATE TABLE IF NOT EXISTS blogs(blog_id INTEGER PRIMARY KEY AUTOINCREMENT, blog_name TEXT UNIQUE, blog_author TEXT, blog_last_update DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')), FOREIGN KEY(blog_author) REFERENCES users(user_name));") #create table for every blog
c.execute("CREATE TABLE IF NOT EXISTS entries(entry_id INTEGER PRIMARY KEY AUTOINCREMENT, entry_blog INTEGER, entry_title TEXT, entry_content TEXT, entry_last_update DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')), FOREIGN KEY(entry_blog) REFERENCES blogs(blog_id));") #create table for every entry

#=========================================================================================================================================

db.commit() #save changes
db.close()  #close database
