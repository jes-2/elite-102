import db
import decimal

def modifybal(id,amt):
    
    db.connect()
    bal = db.csr(f"SELECT balance FROM indentifying WHERE id = '{id}'")
    db.csr(f"UPDATE indentifying SET balance = '{bal+amt}' WHERE id = '{id}'")