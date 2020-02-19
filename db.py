import sqlite3



def conn(path):
    str = path +"\\dataBase.db"
    con = sqlite3.connect(str)
    c = con.cursor()
    return con,c

def getFirstFields(path):
    con,c = conn(path)
    c.execute("SELECT * FROM files")
    rows = c.fetchall()
    con.close()
    return rows


def getEntryFields(path,file):
    con,c = conn(path)
    c.execute("SELECT * FROM entryFields WHERE formName = ?", (file,))
    rows = c.fetchall()
    con.close()
    return rows

def getFieldValues(fieldId,path):
    con,c = conn(path)
    c.execute("SELECT value FROM valuesFields WHERE field = ?", (fieldId,))
    rows = c.fetchall()
    rows.sort()
    con.close()
    return rows

def getEksetasi(path):
    con,c = conn(path)
    c.execute("SELECT * FROM Eksetasi")
    rows = c.fetchall()
    con.close()
    return rows

def createFieldValue(path,value,field):
    con,c = conn(path)
    c.execute("INSERT INTO valuesFields (field,value) VALUES(?,?)", (field,value))

    con.commit()
    con.close()
