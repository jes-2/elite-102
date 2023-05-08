import mysql.connector
from decimal import Decimal

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

def drop_account(id):
    connect()
    csr.execute(f"DELETE FROM login WHERE id = '{id}'")
    csr.execute(f"DELETE FROM indentifying WHERE id = '{id}'")
    cnx.commit()
    getUsers()

def create_account(id,psw,level,name,dob,ssn,pin):
    connect()
    f_dob = dob.split('/')
    
    csr.execute(f"INSERT INTO login(id, psw, admin) VALUES ('{id}','{psw}','{level}')")
    csr.execute(f"INSERT INTO indentifying(id, name, dob, ssn, balance, pin) VALUES ('{id}','{name}','{f_dob[2]}-{f_dob[0]}-{f_dob[1]}','{ssn}',0.00,'{pin}')")
    cnx.commit()

# update the database with our script's user info
def push_userinfo(id=None):
    connect()
    if id == None:
        for i in user_info:
            csr.execute(f"UPDATE indentifying SET name = '{user_info[i]['name']}', dob = '{user_info[i]['dob']}', ssn = '{user_info[i]['ssn']}',pin = '{user_info[i]['pin']}' WHERE id = '{i}'")
            cnx.commit()
    else:
        csr.execute(f"UPDATE indentifying SET name = '{user_info[id]['name']}', dob = '{user_info[id]['dob']}', ssn = '{user_info[id]['ssn']}', pin = '{user_info[id]['pin']}' WHERE id = '{id}'")

def update_login(id,psw):
    connect()
    csr.execute(f"UPDATE login SET psw = '{psw}' WHERE id = '{id}'")
    cnx.commit()
    getUsers()

# update our scripts usertable from the usertable in the database
def getUsers():
    connect()
    csr.execute("SELECT * FROM login")

    for i in csr.fetchall():
        user_info[i[0]] = {'psw':i[1],'name':None,'dob':None,'ssn':None,'balance':None,'pin':None,'admin':i[2]}
    
    csr.execute("SELECT * FROM indentifying")

    for i in csr.fetchall():
        user_info[i[0]]['dob'] = i[2]
        user_info[i[0]]['ssn'] = i[3]
        user_info[i[0]]['name'] = i[1]
        user_info[i[0]]['balance'] = i[4]
        user_info[i[0]]['pin'] = i[5]
    
    csr.close()

# -X removes, X adds
def modifyBal(id,amt,sign):
    connect()
    csr.execute(f"SELECT balance FROM indentifying WHERE id = '{id}'")
    amt = Decimal(amt)
    bal = Decimal(csr.fetchone()[0])
    f = 0
    if sign == '-':
        f = bal-amt
    elif sign == '+':
        f = bal+amt
    csr.execute(f"UPDATE indentifying SET balance = '{str(f)}' WHERE id = '{id}'")
    cnx.commit()
    getUsers()

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
            return [True,'Success',user_info[id]['admin']]
        else:
            return [False,'Incorrect Passkey']
    else:
        return [False,'ID does not exist']