import mysql.connector

current_user = {'usr':'root','psw':'gufhew07'}
current_database = 'users'

data_buffer = None
user_info = {}

cnx = mysql.connector.connect(
    host="localhost",
    user=current_user['usr'],
    password=current_user['psw'],
    database=current_database
)

csr = cnx.cursor()

def connect():
    global cnx,csr
    cnx = mysql.connector.connect(
        host="localhost",
        user=current_user['usr'],
        password=current_user['psw'],
        database=current_database
    )
    csr = cnx.cursor()


def add_Balance(id,amount):
    csr.execute(f"UPDATE indentifying SET balance = balance + {amount} WHERE id = '{id}'")
    cnx.commit()

def remove_balance(id,amount):
    csr.execute(f"UPDATE indentifying SET balance = balance - {amount} WHERE id = '{id}'")
    cnx.commit()

def drop_account(id):
    csr.execute(f"DELETE FROM login WHERE id = '{id}'")
    csr.execute(f"DELETE FROM indentifying WHERE id = '{id}'")
    cnx.commit()

def create_account(id,psw,name,dob,ssn):
    csr.execute(f"INSERT INTO login VALUES ('{id}','{psw}')")
    csr.execute(f"INSERT INTO indentifying VALUES ('{id}','{name}','{dob}','{ssn}',0)")
    cnx.commit()

def getBalance(id):
    csr.execute(f"SELECT balance FROM indentifying WHERE id = '{id}'")
    return csr.fetchone()[0]

# update our scripts usertable from the usertable in the database
def getUsers():
    connect()
    csr.execute("SELECT * FROM login")

    for i in csr.fetchall():
        user_info[i[0]] = {'psw':i[1],'name':None,'dob':None,'ssn':None}
    
    csr.execute("SELECT * FROM indentifying")

    for i in csr.fetchall():
        user_info[i[0]]['dob'] = i[2]
        user_info[i[0]]['ssn'] = i[3]
        user_info[i[0]]['name'] = i[1]
        user_info[i[0]]['balance'] = i[4]
    
    csr.close()

def idExists(id):
    getUsers()
    if id in user_info:
        return True
    else:
        return False
    
def login(id,psw):
    getUsers()
    if idExists(id):
        if user_info[id]['psw'] == psw:
            return [True,'Success']
        else:
            return [False,'Incorrect Passkey']
    else:
        return [False,'ID does not exist']