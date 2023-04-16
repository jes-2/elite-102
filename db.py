import mysql.connector

current_user = {'usr':'root','psw':'gufhew07'}
current_database = 'users'

data_buffer = None

cnx = mysql.connector.connect(
    host="localhost",
    user=current_user['usr'],
    password=current_user['psw'],
    database=current_database
)

csr = cnx.cursor()

