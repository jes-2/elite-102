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

def getUsers():
    csr.execute("SELECT * FROM login")
    return csr.fetchall()

def idExists(id):
    users = getUsers()
    for user in users:
        if user[0] == id:
            return True
    return False
