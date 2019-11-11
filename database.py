import sqlite3

#Open database
conn = sqlite3.connect('database.db')

#Create table
conn.execute('''CREATE TABLE users
		(userId TEXT PRIMARY KEY,
		username TEXT,
        password TEXT,
		name TEXT,
		phone TEXT,

		address TEXT
		)''')

# conn.execute('''CREATE TABLE products
# 		(productId INTEGER PRIMARY KEY AUTOINCREMENT ,
# 		name TEXT,
# 		price TEXTL,
# 		quantity TEXT,
# 		image TEXT,
# 		type TEXT
#
# 		)''')





conn.close()
