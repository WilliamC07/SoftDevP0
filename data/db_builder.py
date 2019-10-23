#====================================================================================================

#db_builder is to be used to create the database and tables.

#====================================================================================================

import sqlite3


def initialize_database(c: sqlite3.Cursor):
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT);")
    c.execute("INSERT OR REPLACE INTO users(name, password) VALUES('admin', 'password');")