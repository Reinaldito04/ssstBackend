import sqlite3

def get_db():
    db = sqlite3.connect('db/db.db')
    return db
