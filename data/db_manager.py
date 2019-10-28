# db_manager is to be used to facilitate database operations.


import sqlite3

DB_FILE = "spew.db"


# add_login takes a username and password and stores it in the users table
# returns an empty string is successful, or an appropriate error message
def add_login(input_name, input_password): 
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    message = ""                  
    c.execute("SELECT * FROM users WHERE user_name = ?;" , (input_name,)) # query rows where the username and input_name match
    if c.fetchone() is None: # if the username does not already exist in the database
        c.execute("INSERT INTO users(user_name, user_password) VALUES(?, ?);" , (input_name, input_password)) # stores the input login credentials in the users table
    else:
        message = "Username exists!" # error message for when the input_name is found in the users table
    db.commit() # save changes
    db.close() # close database
    return message


# verify_login takes a name and password and checks if they exist in any row of the users table
# returns an empty string if the login credentials are found, or an error message if they are not
def verify_login(input_name, input_password): 
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    message = ""
    c.execute("SELECT * FROM users WHERE user_name = ? AND user_password = ?;" , (input_name, input_password)) # query rows where the input name and password match
    if c.fetchone() is None: # if login credentials are not found in the users table
        message = "Login credentials not found!"
    db.commit() # save changes
    db.close() # close database
    return message


# get_usernames_with_blogs is used to list the users that have made blogs
# returns a list of the usernames that have created blogs
def get_usernames_with_blogs(): 
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    usernames = [] #list of all usernames
    c.execute("SELECT blog_author FROM blogs;") # query every blog author in the blogs table
    for tuple in c.fetchall(): # iterate through the rows that are returned
        usernames.append(tuple[0]) # add username from tuple to list of usernames
    db.commit() # save changes
    db.close() # close database
    return list(set(usernames)) # return list without duplicate usernames


# get_blog_id_from_title takes an author and a blog title to find the blog id
# returns the id of the blog if it's found, or None if it is not found
def get_blog_id_from_title(username, blog_title):
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    id = None # initialized at none to fix bugs with viewing entries
    c.execute("SELECT blog_id FROM blogs WHERE blog_author = ? AND blog_name = ?;" , (username, blog_title)) # query blog_id from rows where the inputs match 
    for row in c.fetchall(): # rows that are queried
        id = row[0] # id changed from None to the queried id
    db.commit() # save changes
    db.close() # close database
    return id


# get_blogs_for_username takes a username to compare to authors in the blogs table
# returns a list of every blog they have created, or an empty list if they have not created a blog
def get_blogs_for_username(username): #get names of blogs for a username
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    blogs = [] # initialized empty list of blogs
    c.execute("SELECT blog_name FROM blogs WHERE blog_author = ? ORDER BY blog_last_update DESC;" , (username,)) # query blog_names from rows where the username matches the author
    for tuple in c.fetchall(): # iterates through rows that match the query
        blogs.append(tuple[0]) # add blog name from tuple to list
    db.commit() # save changes
    db.close() # close database
    return blogs


# create_blog_for_username takes a username and title and creates a new blog in the blogs table
# returns an empty string if successful, or an appropriate error message
def create_blog_for_username(username, blog_title):
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    message = ""
    c.execute("SELECT * FROM blogs WHERE blog_name = ? AND blog_author = ?;" , (blog_title, username)) # query rows where the name and author match
    if c.fetchone() is None: # if there are no rows that match the query
        c.execute("INSERT INTO blogs(blog_name, blog_author) VALUES (?, ?);" , (blog_title, username)) # insert the new blog information into the table
    else:
        message = "Blog already exists!" 
    db.commit() # save changes
    db.close() # close database
    return message


# get_entries_for_blog takes a blog id and returns the entries for that blog
# returns a list of tuples with the title and the content of each entry in the blog
def get_entries_for_blog(blog_id):
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    entries = [] # initialize list of entries
    c.execute("SELECT * FROM entries WHERE entry_blog = ? ORDER BY entry_last_update DESC;" , (blog_id,)) # query rows in entries table where the blog id matches
    for tuple in c.fetchall(): # query uses ORDER BY to return the list of tuples ordered from most recently updated
        entries.append(tuple[2:4]) # append tuple containing the title and content 
    db.commit() # save changes
    db.close() # close database
    return entries


# is_owner takes a username and blog and checks if that user is the author of the blog
# returns an True if the user is the owner, or False if they are not
def is_owner(username, blog_id): #return boolean is a user is owner of a blog
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    ownership = False # initialize boolean to False
    c.execute("SELECT * FROM blogs WHERE blog_id = ? AND blog_author = ?;" , (blog_id, username)) # query rows where the id and author match
    if c.fetchone() is not None: # if there is such row
        ownership = True # the user is the author of the blog
    db.commit() # save changes
    db.close() # close database
    return ownership


# add_entry takes a title, content, and blog and stores that information in the entries table
# returns an empty string if successful, or an appropriate error message
def add_entry(entry_title, entry_content, blog_id): 
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    message = ""
    c.execute("SELECT * FROM entries WHERE entry_blog = ? AND entry_title = ?;" , (blog_id, entry_title)) # query rows where the information matches 
    if c.fetchone() is None: # if there is no such row
        c.execute("INSERT INTO entries(entry_title, entry_content, entry_blog) VALUES (?, ?, ?);" , (entry_title, entry_content, blog_id)) # insert the information in the entries table
    else:
        message = "Entry title already exists in this blog!"
    db.commit() # save changes
    db.close() # close database
    return message


# get_entry_id takes the title of an entry and the id of the blog to which it belongs
# returns the id of the entry if the entry is found, otherwise it will return None
def get_entry_id(entry_title, blog_id):
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    id = None # initialized at none to fix bugs with viewing entries
    c.execute("SELECT entry_id FROM entries WHERE entry_title = ? AND entry_blog = ?;" , (entry_title, blog_id)) # query entry_ids for rows where the input_title and blog_id are found
    for row in c.fetchall(): # rows that are returned
        id = row[0] # id changed from None to the queried id
    db.commit() # save changes
    db.close() # close database
    return id


# remove_entry will remove an entry from the entries table given the id
# returns an empty string if successful, or an appropriate error message
def remove_entry(entry_id):
    db = sqlite3.connect(DB_FILE) # open file
    c = db.cursor() # facilitate db ops
    c.execute("SELECT * FROM entries WHERE entry_id = ?;" , (entry_id,)) # query rows in entries table where the id matches the input
    message = ""
    if c.fetchone() is not None: # if there is a row with the id
        c.execute("DELETE FROM entries WHERE entry_id = ?;" , (entry_id,)) # the row is deleted from the table
    else:
        message = "Entry does not exist!" # error message when the id is not found
    db.commit() # save changes
    db.close() # close database
    return message
