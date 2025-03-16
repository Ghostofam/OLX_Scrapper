import sqlite3

db_name = "olx_db"

connection = sqlite3.connect(db_name)
print(f"Connected to database: {db_name}")

cursor = connection.cursor()

#cursor.execute("""
#    CREATE TABLE IF NOT EXISTS Link(
#        link_id INTEGER PRIMARY KEY,
#        link_url TEXT
#    );               
#""")


#cursor.execute("""
#    CREATE TABLE IF NOT EXISTS Mobiles(
#        mob_id INTEGER PRIMARY KEY,
#        name TEXT,
#        price INTEGER,
#        location TEXT,
#        date DATETIME,
#        description TEXT,
#        links TEXT,
#        FOREIGN KEY (links) REFERENCES Link(link_url)
#    );
#""")

for row in cursor.execute("SELECT * From Mobiles"):
    print(row)


connection.commit()
connection.close()
print("Database schema created successfully.")