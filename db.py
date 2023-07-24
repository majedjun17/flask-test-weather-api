import sqlite3

# Connect to the SQLite database
# This will create a new file named 'example.db' if it doesn't exist
conn = sqlite3.connect('general.db')

# Create a cursor object
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE weather
    (id text, temp REAL, humidity REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
''')

# # Insert a row of data
# c.execute("INSERT INTO event (id, rank, long, lat) VALUES (?, ?, ?, ?)", 
#           ('hiii', 12, 32.9, 33.66))

# # Save (commit) the changes
conn.commit()



# Retrieve data
# r = c.execute('SELECT * FROM event WHERE id = ? AND created_at >= datetime("now", "-6 hours")', ('639QKBmRfQYgMitrgS',))
# for i in r:
#     print(i)
conn.close()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
