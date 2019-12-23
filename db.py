import sqlite3



def conn(path):
    str = path +"\db.db"
    con = sqlite3.connect(str)
    c = con.cursor()
    return con,c

def getFirstFields(path):
    con,c = conn(path)
    c.execute("SELECT * FROM firstWindowButtons")
    rows = c.fetchall()
    con.close()
    return rows


def getEntryFields(path):
    con,c = conn(path)
    c.execute("SELECT * FROM entryFields")
    rows = c.fetchall()
    con.close()
    return rows

def getFieldValues(fieldId,path):
    con,c = conn(path)
    c.execute("SELECT value FROM valuesFields WHERE field = ?", (fieldId,))
    rows = c.fetchall()
    rows.sort()
    con.close()
    print(rows)
    return rows


def createFieldValue(value,field):
    con,c = conn()
    print(field,value)
    c.execute("INSERT INTO valuesFields (field,value) VALUES(?,?)", (field,value))

    con.commit()
    con.close()
