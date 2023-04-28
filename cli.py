import db

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
    
    def main():
        while True:
            if session.session_login == None:
                print('Invalid session')
                break
            print(u'\u2500' * 20)
            print(f"Welcome {user_info['name']} ({session.session_login['id']})")
            input('')
    
    def getBalance():
        print(db.getBalance(session.session_login['id']))

session.login()