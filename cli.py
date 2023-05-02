import db
import random

def isInt(x):
    try:
        int(x)
        return True
    except:
        return False

class session:
    options = {
        1: {
            'option_name':'Get Balance',
            'description':'Get the balance of your account',
            'function':None
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
            id = int(input("ID: "))
            pk = input("PK: ")

            success = db.login(id,pk)

            if success[0]:
                print(success[1])
                session.session_login = {'id':id,'pk':pk}
                db.getUsers()
                global user_info
                user_info = db.user_info[id]
                session.main()
                break
            else:
                print(success[1])
                session.session_login = None
                print('Would you like to go back?')
                ch = input(" > ")
                if (ch=="y" or ch=="yes"):
                    session.menu()
                    break
    
    def signup():
        print(f"NilBank\n{'-'*20}\nCreate Account\n{'-'*20}")
        
        n=None
        d=None
        s=None
        p=None

        # Get Name
        print('Legal Name:')
        n = input(' > ')

        # Get DOB
        while True:
            print('Date of Birth (XX/XX/XXXX):')
            d = input(' > ')
            if len(d) == 10 and d[2] == '/' and d[5] == '/':
                break
            else:
                print('\nInvalid date format\n')

        # Get SSN
        while True:
            print('Social Security Number (XXX-XX-XXXX):')
            s = input(' > ')
            if len(s) == 11 and s[3] == '-' and s[6] == '-':
                break
            else:
                print('\nInvalid SSN format\n')

        # Get Password
        while True:
            print('Password (>6 chars) :')
            p = input(' > ')
            if not len(p) > 6:
                print('\nPassword must be longer than 6 characters\n')
            else:
                print('Confirm Password:')
                cp = input(' > ')
                if p == cp:
                    break
                else:
                    print('\nPasswords do not match\n')
        
        # Create Account procedure
        db.getUsers()
        while True:
            randId = random.randint(100000000,999999999)
            if not randId in db.user_info:
                db.create_account(randId,p,n,d,s)
                break
        
        print(f"Account created with ID {randId}, please login.")
        session.menu()

    def forgot_psw():
        db.getUsers()
        print(f"Help\n\nForgot Password\n{'-'*20}")
        
        while True:
            print('Enter ID:')
            id = input(' > ')
            if id.isdigit() and int(id) in db.user_info:
                id = int(id)
                print('Enter SSN:')
                ssn = input(' > ')
                if db.user_info[id]['ssn'] == ssn:
                    print('Great!')
                    p1=None
                    while True:
                        print('Enter new password:')
                        p1 = input(' > ')
                        if not len(p1) >= 6:
                            print('Password must be longer than 6 characters')
                        else:
                            break
                    print('Confirm new password:')
                    p2 = input(' > ')
                    if p1 == p2:
                        print('Password changed successfully!')
                        db.update_login(id,p1)
                        print(db.user_info)
                        session.menu()
                        break
                    else:
                        print('Passwords do not match')
                        continue
            else:
                print('Invalid ID')
                continue


    def main():
        while True:
            if session.session_login == None:
                print('Invalid session')
                break
            print(u'\u2500' * 20)
            print(f"Welcome {user_info['name']} (ID {session.session_login['id']})")
            input('')
    
    def getBalance():
        db.getUsers()
        return db.user_info[session.session_login[session.session_login['id']]]['balance']
    
    def deposit(id,x):
        db.getUsers()
        db.user_info[session.session_login[id]]['balance'] += x

session.menu()