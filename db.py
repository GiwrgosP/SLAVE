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
    c.execute("SELECT objectId,nameId,sort FROM widget WHERE widgetId = ?", (widget,))
    rows = c.fetchall()
    con.close()
    return rows[0]

def getWidgetName(path,name):
    con,c = conn(path)
    print(name)
    c.execute("SELECT nameVal FROM widgetNames WHERE nameId = ?", (name,))
    rows = c.fetchall()
    con.close()
    print(rows)
    return rows[0]

def getWidgetMenus(path,widgetId):
    con,c = conn(path)
    c.execute("SELECT * FROM widgetMenus WHERE widgetId = ?", (widgetId,))
    rows = c.fetchall()
    con.close()
    return rows

def getValues(path,widgetMenuId):
    con,c = conn(path)
    c.execute("SELECT value FROM menuValues WHERE widgetMenuId = ?", (widgetMenuId,))
    rows = c.fetchall()
    con.close()
    temp = list()
    for row in rows:
        temp.append(row[0])
    return temp

def getEksetasi(path):
    con,c = conn(path)
    c.execute("SELECT * FROM Eksetasi")
    rows = c.fetchall()
    con.close()
    return rows

def createValue(path,value,field):
    con,c = conn(path)
    c.execute("INSERT INTO menuValues (widgetMenuId,value) VALUES(?,?)", (field,value,))
    con.commit()
    con.close()

def getPetWeightIndex(path,petId):
    con,c = conn(path)
    c.execute("SELECT average,tooMuch FROM petWeightIndex WHERE petId = ?", (petId,))
    rows = c.fetchall()
    con.close()
    return rows[0]

def getPetAgeIndex(path,petId):
    con,c = conn(path)
    c.execute("SELECT adult,elder FROM petAgeIndex WHERE petId = ?", (petId,))
    rows = c.fetchall()
    con.close()
    return rows[0]

def getCardioAnalisVal(path,testId):
    con,c = conn(path)
    c.execute("SELECT value FROM cardiologicalAnalysisVal WHERE testId = ?", (testId,))
    rows = c.fetchall()
    con.close()
    return rows
