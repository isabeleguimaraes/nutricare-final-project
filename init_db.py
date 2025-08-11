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

#Create a patient_nutri_link table (to manage relationship between patient and nutritionist and requests)
cursor.execute(""" CREATE TABLE IF NOT EXISTS patient_nutri_link (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               patient_id INTEGER,
               nutri_id INTEGER,
               status TEXT,
               FOREIGN KEY (patient_id) REFERENCES users(id),
               FOREIGN KEY (nutri_id) REFERENCES users(id)
               )
               """)

#Create a meals table (to manage patient's diet)
cursor.execute(""" CREATE TABLE IF NOT EXISTS diet (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               link_id INTEGER,
               meal_type TEXT,
               combination TEXT,
               item TEXT,
               FOREIGN KEY (link_id) REFERENCES patient_nutri_link(id)
               )
               """)

# Create progress Table to log and track patient's progress



#Commiting the table creation
conn.commit()
#Closing the connection
conn.close()