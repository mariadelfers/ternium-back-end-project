import mysql.connector

cnx = mysql.connector.connect(user='user', password='Password123.',
                              host='localhost',
                              database='chocolate')

cursor = cnx.cursor()

query = ("SELECT name FROM pet")

cursor.execute(query)

for name in cursor:
  print name

cursor.close()

cnx.close()