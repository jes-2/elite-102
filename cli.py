import db
import random
import decimal

def toDec(x):
    try:
        d=decimal.Decimal(str(x))
        return d
    except:
        return None
    

def isInt(x):
    try:
        int(x)
        return True
    except:
        return False
    
def deposit():
    db.getUsers()
    print(f"Deposit\n{'-'*20}")
    print('\nPlease enter pin')
    p = input(' > ')
    if p != db.user_info[session.session_login['id']]['pin']:
        print('Incorrect pin')
        return
    print("How much would you like to deposit?")
    while True:
        x = input(' > ')
        if x == None or not '.' in x:
            print('Invalid input')
        else:
            db.modifyBal(session.session_login['id'],x,'+')
            db.getUsers()
            print(f"New Balance: {db.user_info[session.session_login['id']]['balance']}")
            break
        
            
def withdraw():
    db.getUsers()
    print(f"Withdraw\n{'-'*20}")
    print('\nPlease enter pin')
    p = input(' > ')
    if p != db.user_info[session.session_login['id']]['pin']:
        print('Incorrect pin')
        return
    print("How much would you like to withdraw?")
    while True:
        x = input(' > ')
        if x == None or not '.' in x:
            print('Invalid input')
        else:
            db.modifyBal(session.session_login['id'],x,'-')
            db.getUsers()
            print(f"New Balance: {db.user_info[session.session_login['id']]['balance']}")
            break
            
def create_user():
    print(f"\nCreate User\n{'-'*20}")
    print("\nFormat - id:pk(>6):level(0-1)\n")
    inf = input(" > ").split(':')
    for i,v in enumerate(inf):
        if v == None:
            print(f'Missing {inf[i]}')
            return
    if len(inf[1]) < 6:
        print('PK must be >6')
        return
    elif not isInt(inf[2] or not (int(inf[2]) > 1 or int(inf[2]) < 0)):
        print('Level must be 0 or 1')
        return
    elif db.idExists(inf[0]):
        print('ID already exists')
        return
    
    print("\nName")
    n = input(" > ")
    print("\nDOB (MM/DD/YYYY)")
    d = input(" > ")
    print("\nSSN")
    s = input(" > ")
    print("\nPIN")
    p = input(" > ")
    if not s.isdigit() or len(s) != 9:
        print('Invalid SSN')
        return
    elif not p.isdigit() or not len(p) != 4:
        print('Invalid PIN')
        return
    db.create_account(inf[0],inf[1],inf[2],n,d,s,p)

def delete_user():
    db.getUsers()
    print(f"\nDelete User\n{'-'*20}")
    for i in db.user_info:
        print(f"ID: {i} - {db.user_info[i]['name']}")
    print("\nFormat - id\n")
    id = input(" > ")
    if id == None:
        return
    elif not isInt(id):
        print('ID must be an integer')
        return
    
    id = int(id)
    if not db.idExists(id):
        print('ID does not exist')
        return
    db.drop_account(id)

def dev():
    while True:
        if not session.session_login['admin'] == 1 or session.session_login == None:
            print(' ! ACCESS_DENIED')
            break
        print(f"{'-'*20}\nDeveloper Options\n{'-'*20}")
        for i,v in session.dev_options.items():
            print(f"{i}: {v['option_name']} - {v['description']}")
        ch = input(' > ')
        if isInt(ch) and int(ch) in session.dev_options.keys():
            ch = int(ch)
            if ch == -1:
                break
            else:
                if session.dev_options[ch]['function'] == None:
                    print(' ! Function not implemented')
                else:
                    session.dev_options[ch]['function']()

def forgot_PIN():
    print(f"\nForgot PIN\n{'-'*20}")
    print('\n - Please enter your SSN')
    attempts = 0
    while True:
        s = input(' > ')
        if not s.isdigit() and len(s) != 9:
            print(' ! Invalid SSN')
        else:
            db.getUsers()
            if db.user_info[session.session_login['id']]['ssn'] != s:
                print(' ! Incorrect SSN')
                continue
            else:
                print(' - Please enter new PIN')
                while True:
                    p = input(' > ')
                    if not p.isdigit() or len(p) != 4:
                        print('! Invalid PIN')
                    else:
                        db.user_info[session.session_login['id']]['pin'] = p
                        db.push_userinfo()
                        db.getUsers()
                        print(' - PIN changed\n')
                        break
                break

def change_PIN():
    attempts = 0
    threshold = 3
    print(f"\nChange PIN\n{'-'*20}")
    print('\n - Please enter current PIN')
    while True:
        if attempts > threshold:
            print(" - Forgot PIN?")
            ch = input(' > ')
            if ch == 'y' or ch == 'yes':
                forgot_PIN()
                break
            else:
                threshold += 3
                continue
        p = input(' > ')
        if p != db.user_info[session.session_login['id']]['pin']:
            print(' ! Incorrect pin')
            attempts += 1
        else:
            print(' - Please enter new PIN')
            while True:
                p = input(' > ')
                if not p.isdigit() or len(p) != 4:
                    print('! Invalid PIN')
                else:
                    db.user_info[session.session_login['id']]['pin'] = p
                    db.push_userinfo()
                    db.getUsers()
                    print(' - PIN changed\n')
                    break
            break
    print('')

def mng_account():
    db.getUsers()
    print(f"{'-'*20}\nAccount Options\n{'-'*20}")
    print(f"    ID {session.session_login['id']}\nName {db.user_info[session.session_login['id']]['name']}\nBalance ${db.user_info[session.session_login['id']]['balance']}\n")
    while True:
        print('')
        for i,v in session.account_options.items():
            print(f"{i}: {v['option_name']} - {v['description']}")
        ch = input(' > ')
        if isInt(ch) and int(ch) in session.account_options.keys():
            if ch == '-1':
                break
            else:
                ch = int(ch)
                if session.account_options[ch]['function'] == None:
                    print(' ! Function not implemented')
                else:
                    session.account_options[ch]['function']()
                    print("")

class session:
    dev_options = {
        0: {
            'option_name':'Elevate User',
            'description':"Elevate user's permissions",
            'function':None
        },
        1: {
            'option_name':'Delete User',
            'description':'Delete user from database',
            'function': delete_user
        },
        2: {
            'option_name':'Create User',
            'description':'Create user in database',
            'function': create_user
        },
        3: {
            'option_name':'Update User',
            'description':'Update user in database',
            'function':None
        },
        -1: {
            'option_name':'Exit',
            'description':'Exit developer options',
            'function':None
        
        }
    }

    account_options = {
        0: {
            'option_name':'Change PIN',
            'description':'Change your PIN',
            'function':change_PIN
        },
        -1: {
            'option_name':'Exit',
            'description':'Exit account options',
            'function':None
        }
    }

    options = {
        0: {
            'option_name':'Logout',
            'description':'End session',
            'function':None
        },
        1: {
            'option_name':'Deposit',
            'description':'Deposit money into your account',
            'function': deposit
        },
        2: {
            'option_name':'Withdraw',
            'description':'Withdraw money from your account',
            'function': withdraw
        },
        3: {
            'option_name':'Account',
            'description':'Manage your account',
            'function': mng_account
        }
    }
    user_info = None
    session_login = None

    def menu():
        while True:
            print("""
            NilBank
            
            1. Login
            2. Sign Up
            3. Forgot Password?""")
            ch = input(' > ')

            if ch == '1':
                session.login()
            elif ch == '2':
                session.signup()
            elif ch == '3':
                session.forgot_psw()
    
    def login():
        while True:
            id = int(input(" - ID "))
            pk = input(" - PK ")

            success = db.login(id,pk)

            if success[0]:
                print(success[1])
                session.session_login = {'id':id,'pk':pk,'admin':success[2]}
                db.getUsers()
                global user_info
                user_info = db.user_info[id]
                session.main()
                break
            else:
                print(success[1])
                session.session_login = None
                print(' - Would you like to go back?')
                ch = input(" > ")
                if (ch=="y" or ch=="yes"):
                    session.menu()
                    break
    
    def signup():
        print(f"NilBank\n{'-'*20}\nCreate Account\n{'-'*20}")
        
        n=None
        d=None
        s=None
        pk=None
        p=None

        # Get Name
        print(' - Legal Name:')
        n = input(' > ')

        # Get DOB
        while True:
            print(' - Date of Birth (XX/XX/XXXX):')
            d = input(' > ')
            if len(d) == 10 and d[2] == '/' and d[5] == '/':
                break
            else:
                print('\n ! Invalid date format\n')

        # Get SSN
        while True:
            print(' - Social Security Number (XXX-XX-XXXX):')
            s = input(' > ')
            if len(s) == 11 and s[3] == '-' and s[6] == '-':
                break
            else:
                print('\n ! Invalid SSN format\n')

        # Get Password
        while True:
            print(' - Password (>6 chars) :')
            pk = input(' > ')
            if not len(pk) > 6:
                print('\n ! Password must be longer than 6 characters\n')
            else:
                print(' - Confirm Password:')
                cp = input(' > ')
                if pk == cp:
                    break
                else:
                    print('\n ! Passwords do not match\n')

        #Get PIN
        while True:
            print(' - PIN (4 chars):')
            p = input(' > ')
            if not len(p) == 4:
                print('\n ! PIN must be 4 characters\n')
            else:
                print(' - Confirm PIN:')
                cp = input(' > ')
                if p == cp:
                    break
                else:
                    print('\n ! PINs do not match\n')
        
        # Create Account procedure
        db.getUsers()
        while True:
            randId = random.randint(100000000,999999999)
            if not randId in db.user_info:
                db.create_account(randId,pk,n,d,s,p)
                break
        print(f"Account created with ID {randId}, please login.")
        session.menu()

    def forgot_psw():
        db.getUsers()
        print(f"Help\n\nForgot Password\n{'-'*20}")
        
        while True:
            print(' - Enter ID')
            id = input(' > ')
            if id.isdigit() and int(id) in db.user_info:
                id = int(id)
                print(' - Enter SSN')
                ssn = input(' > ')
                if db.user_info[id]['ssn'] == ssn:
                    print(' - Great!')
                    p1=None
                    while True:
                        print(' - Enter new password')
                        p1 = input(' > ')
                        if not len(p1) >= 6:
                            print(' ! Password must be longer than 6 characters')
                        else:
                            break
                    print('   Confirm new password:')
                    p2 = input(' > ')
                    if p1 == p2:
                        print('\n - Password changed successfully!')
                        db.update_login(id,p1)
                        session.menu()
                        break
                    else:
                        print(' ! Passwords do not match')
                        continue
                else:
                    print(' ! Invalid SSN (XXX-XX-XXXX)')
            else:
                print('\n - Invalid ID')
            print(' - Try again?')
            ch = input(' > ')
            if ch == 'n' or ch == 'no':
                break


    def main():
        if session.session_login == None:
            print('Invalid session')
            return
        if session.session_login['admin'] == 1:
            dev()
            return
        print(u'\u2500' * 20)
        print(f"Welcome {user_info['name']} (ID {session.session_login['id']})")
        while True:
            for i,v in session.options.items():
                print(f"{i}. {v['option_name']}")
            ch=input(' > ')
            if ch.isdigit() and int(ch) in session.options.keys():
                ch = int(ch)
                if ch == 0:
                    session.session_login = None
                    print(' - Logged out')
                    break
                if session.options[ch]['function'] == None:
                    print(' ! Function not implemented')
                else:
                    session.options[ch]['function']()
            else:
                print('Invalid option')



session.menu()