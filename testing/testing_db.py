import mysql.connector

cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="gufhew07",
  database="users"
)

cursor = cnx.cursor()

cursor.execute('SELECT * FROM login')

print(cursor.fetchall())