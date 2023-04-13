import sqlalchemy

engine = None

def createEngine(user,psw,db):
    global engine
    url = sqlalchemy.URL.create(
        "postgresql+psycopg2",
        username=user,
        password=psw,
        host="localhost",
        database=db
    )
    try:
        engine = sqlalchemy.create_engine(url, echo=True)
        return
    except:
        print(__file__+": Something went wrong.")

def execute(comm):
    global engine
    if engine == None:
        print(__file__+".py: No engine created")
    else:
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(comm))
            return result.all()
