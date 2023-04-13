import sqlalchemy as sql

engine = sql.create_engine("postgresql://root:gufhew07@localhost:3306")
con = engine.connect()

def exe(command):
    if not type(command) == 'str':
        print(__file__+": command is not a string")
    else:
        with engine.connect() as connection:
            connection.execute(sql.text(command))
            connection.commit()
            print(__file__+": executed")