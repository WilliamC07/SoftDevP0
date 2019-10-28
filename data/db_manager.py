#========================================================================================

#db_manager is to be used to facilitate operations from frontend/backend to the database.

#========================================================================================

import sqlite3

def add_login(input_name, input_password): #facilitate adding new login credentials
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    c.execute("SELECT * FROM users WHERE user_name = ?;" , (input_name,)) #all instances of name in database
    if c.fetchone() is None: #if name is not found in database
        c.execute("INSERT INTO users(user_name, user_password) VALUES(?, ?);" , (input_name, input_password)) #add login credentials
        db.commit() #save changes
        db.close() #close database
        return ""
    else:
        db.commit() #save changes
        db.close() #close database
        return "Username exists!"

#print(add_login("admin", "password")) #test adding login credentials with new name
#print(add_login("admin", "password")) #test adding login credentials with existing name


def verify_login(input_name, input_password): #verify login credentials
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    c.execute("SELECT * FROM users WHERE user_name = ? AND user_password = ?;" , (input_name, input_password)) #any rows where the inputs match
    if c.fetchone() is not None: #if login credentials are found in database
        db.commit() #save changes
        db.close() #close database
        return ""
    else:
        db.commit() #save changes
        db.close() #close database
        return "Login credentials not found!"

#print(verify_login("admin", "password")) #test existing login
#print(verify_login("admin", "fakePassword")) #test fake login credentials


def get_usernames_with_blogs(): #get usernames from blog titles
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    usernames = [] #list of all usernames
    c.execute("SELECT blog_author FROM blogs;") #all blog authors
    for tuple in c.fetchall(): #rows that are returned
        usernames.append(tuple[0]) #add  author/user name from tuple to list
    db.commit() #save changes
    db.close() #close database
    return list(set(usernames)) #return without duplicate usernames

#print(get_usernames_with_blogs())


def get_blog_id_from_title(username, blog_title):
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    c.execute("SELECT blog_id FROM blogs WHERE blog_author = ? AND blog_name = ?;" , (username, blog_title))
    for row in c.fetchall(): #rows that are returned
        id = row[0]
    db.commit() #save changes
    db.close() #close database
    return id


def get_blogs_for_username(username): #get names of blogs for a username
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    blogNames = [] #list of all the blog titles
    c.execute("SELECT blog_name FROM blogs WHERE blog_author = ? ORDER BY blog_last_update DESC;" , (username,)) #all instances of name in database
    for tuple in c.fetchall(): #rows that are returned
        blogNames.append(tuple[0]) #add blog name from tuple to list
    db.commit() #save changes
    db.close() #close database
    return blogNames

#print(get_blogs_for_username("admin"))


def create_blog_for_username(username, blog_title):
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    status = ""
    c.execute("SELECT * FROM blogs WHERE blog_name = ? AND blog_author = ?;" , (blog_title, username))
    if c.fetchone() is None:
        c.execute("INSERT INTO blogs(blog_name, blog_author) VALUES (?, ?);" , (blog_title, username))
    else:
        status = "Blog already exists!"
    db.commit() #save changes
    db.close() #close database
    return status #return empty string if works

#print(create_blog_for_username("admin", "admin's blog"))
#print(create_blog_for_username("admin", "admin's blog"))
#print(create_blog_for_username("admin", "admin's other blog"))


def get_entries_for_blog(blog_id): #get every entry of a blog as tuples (title,content)
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    entries = [] #list of tuples
    c.execute("SELECT * FROM entries WHERE entry_blog = ? ORDER BY entry_last_update DESC;" , (blog_id,))
    for tuple in c.fetchall():
        entries.append(tuple[2:4])
    db.commit() #save changes
    db.close() #close database
    return entries


def is_owner(username, blog_id): #return boolean is a user is owner of a blog
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    ownership = False
    c.execute("SELECT * FROM blogs WHERE blog_id = ? AND blog_author = ?;" , (blog_id, username))
    if c.fetchone() is not None:
        ownership = True
    db.commit() #save changes
    db.close() #close database
    return ownership


def add_entry(entry_title, entry_content, blog_id): #CHANGED INPUTS!
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    status = ""
    c.execute("SELECT * FROM entries WHERE entry_blog = ? AND entry_title = ?;" , (blog_id, entry_title))
    if c.fetchone() is None:
        c.execute("INSERT INTO entries(entry_title, entry_content, entry_blog) VALUES (?, ?, ?);" , (entry_title, entry_content, blog_id))
    else:
        status = "Entry title already exists in this blog!"
    db.commit() #save changes
    db.close() #close database
    return status #return empty string if works, else return error message


def get_entry_id(entry_title, blog_id):
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    c.execute("SELECT entry_id FROM entries WHERE entry_title = ? AND entry_blog = ?;" , (entry_title, blog_id))
    if c.fetchone() is not None:
        id = c.fetchone()
    else:
        id = None
    db.commit() #save changes
    db.close() #close database
    return id


def remove_entry(entry_id):
    db = sqlite3.connect("spew.db") #open file
    c = db.cursor() #facilitate db ops
    c.execute("SELECT * FROM entries WHERE entry_id = ?;" , (entry_id,))
    status = ""
    if c.fetchone() is None:
        status = "Entry does not exist!"
    else:
        c.execute("DELETE FROM entries WHERE entry_id = ?;" , (entry_id,))
    db.commit() #save changes
    db.close() #close database
    return status
