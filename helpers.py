import sqlite3

# DATABASE INTERACTION

DB_NAME = 'database/nutricare.db'

# Insert, Delete, Update
def write_to_db(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# Select All Information
def read_all_from_db(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()

    return result

# Select One Information
def read_one_from_db(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()

    return result






