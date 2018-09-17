import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="moreillon",
  passwd="00174000",
  database="nameboards"
)

MySQL_table = "nameboards"

mycursor = mydb.cursor()

SQL_query = "DROP TABLE IF EXISTS %s"
mycursor.execute(SQL_query % MySQL_table)

SQL_query = "CREATE TABLE %s (id INT AUTO_INCREMENT PRIMARY KEY, member_name VARCHAR(255), group_name VARCHAR(255), presence BOOLEAN, location VARCHAR(255), arrival VARCHAR(255) )"
mycursor.execute(SQL_query % MySQL_table)

SQL_query = "SHOW columns FROM %s"
mycursor.execute(SQL_query % MySQL_table)

print(mycursor.fetchall())
