import sqlite3

#Create a connection with the database
conn = sqlite3.connect('database/nutricare.db')

#Create a cursor to navigate through the database
cursor = conn.cursor()

#Create a users table (to manage login and id)
cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               email TEXT UNIQUE,
               hash TEXT,  
               role TEXT)
""")

#Create a diet table (to manage relationship between patient and nutritionist and requests)
cursor.execute(""" CREATE TABLE IF NOT EXISTS diet (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               nutri_id INTEGER,
               status TEXT,
               FOREIGN KEY (user_id) REFERENCES users(id),
               FOREIGN KEY (nutri_id) REFERENCES users(id)
               )
               """)

#Create a meals table (to manage patient's diet)
cursor.execute(""" CREATE TABLE IF NOT EXISTS meals (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               diet_id INTEGER,
               meal_type TEXT,
               option TEXT,
               item TEXT,
               FOREIGN KEY (diet_id) REFERENCES diet(id)
               )
               """)


#Commiting the table creation
conn.commit()
#Closing the connection
conn.close()