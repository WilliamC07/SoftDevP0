# db_builder is to be used to initialize the database 
# with the tables for users, blogs, and entries.


import sqlite3

db = sqlite3.connect("spew.db") # open if file exists, otherwise create
c = db.cursor()                 # facilitate db ops


# create a users table that stores an id, the user's name, and the user's password
c.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT UNIQUE, user_password TEXT);")

# create a blogs table that stores an id, the blog's name, the blog's author, and the last update time of the blog 
c.execute("CREATE TABLE IF NOT EXISTS blogs(blog_id INTEGER PRIMARY KEY AUTOINCREMENT, blog_name TEXT, blog_author TEXT, blog_last_update DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')), FOREIGN KEY(blog_author) REFERENCES users(user_name));")

# create a entries table that stores an id, the id of the blog to which the entry belongs, the entry's title, the contents of the entry, and the last update time of the entry
c.execute("CREATE TABLE IF NOT EXISTS entries(entry_id INTEGER PRIMARY KEY AUTOINCREMENT, entry_blog INTEGER, entry_title TEXT, entry_content TEXT, entry_last_update DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')), FOREIGN KEY(entry_blog) REFERENCES blogs(blog_id));")


db.commit() # save changes
db.close()  # close database
