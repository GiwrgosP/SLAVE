import sqlite3

def conn():
    con = sqlite3.connect("C:\Python37-64\sof\db.db")  #++++++++++++++++++++++ ALLAGI URL************* MIN ALLAXEIS TO ONOMA TOU ARXEIOU
    c = con.cursor()
    return con,c

def getEntryFields():
    con,c = conn()
    c.execute("SELECT * FROM entryFields")
    rows = c.fetchall()
    con.close()
    return rows

def getFieldValues(fieldId):
    con,c = conn()
    c.execute("SELECT value FROM valuesFields WHERE field = ?", (fieldId,))
    rows = c.fetchall()
    con.close()
    print(rows)
    return rows


def createFieldValue(value,field):
    con,c = conn()
    print(field,value)
    c.execute("INSERT INTO valuesFields (field,value) VALUES(?,?)", (field,value))

    con.commit()
    con.close()
