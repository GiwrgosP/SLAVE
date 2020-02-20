import sqlite3

def conn(path):
    str = path +"\\dataBase.db"
    con = sqlite3.connect(str)
    c = con.cursor()
    return con,c

def getFile(path):
    con,c = conn(path)
    c.execute("SELECT * FROM files")
    rows = c.fetchall()
    con.close()
    return rows


def getForm(path,file):
    con,c = conn(path)
    c.execute("SELECT * FROM form WHERE fileId = ?", (file,))
    rows = c.fetchall()
    con.close()
    return rows

def getWidget(path,widget):
    con,c = conn(path)
    c.execute("SELECT objectId,nameId FROM widget WHERE widgetId = ?", (widget,))
    rows = c.fetchall()
    con.close()
    return rows[0]

def getWidgetName(path,name):
    con,c = conn(path)
    c.execute("SELECT nameVal FROM widgetName WHERE nameId = ?", (name,))
    rows = c.fetchall()
    con.close()
    return rows[0]

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
