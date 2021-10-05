import sqlite3

con = sqlite3.connect('SOF.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS python
               (question, link, date)''')

# Save (commit) the changes
con.commit()

# Close connections
con.close()