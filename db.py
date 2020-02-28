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

def getForm(path,widgetId):
    con,c = conn(path)
    c.execute("SELECT widgetId FROM form WHERE fileId = ?", (widgetId,))
    rows = c.fetchall()
    con.close()
    return rows

def getWidget(path,widget):
    con,c = conn(path)
    c.execute("SELECT objectId,name,nameVal,sort FROM widget WHERE widgetId = ?", (widget,))
    rows = c.fetchall()
    con.close()
    return rows[0]

def getWidgetMenus(path,widgetId):
    con,c = conn(path)
    c.execute("SELECT menuId FROM widgetMenus WHERE widgetId = ?", (widgetId,))
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




    objectList = {"menuEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "spinbox": lambda self,ent:formEntries.spinBox(self,ent),\
    "entry": lambda self,ent:formEntries.entry(self,ent),\
    "mediMenu": lambda self,ent:formEntries.medicMenuEnt(self,ent),\
    "ageSpinBoxEnt": lambda self,ent:formEntries.ageSpinBoxEnt(self,ent),\
    "ecgMenuEnt": lambda self,ent:formEntries.ecgMenuEnt(self,ent),\
    "flowButtonEnt": lambda self,ent:formEntries.flowButtonEnt(self,ent),\
    "checkUpSpinBoxEn": lambda self,ent:formEntries.checkUpSpinBoxEn(self,ent),\
    "nameAitEntryEnt": lambda self,ent:formEntries.nameAitEntryEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "dogDMVD1CardiologicalAnalysisListBoxEnt": lambda self,ent:formEntries.dogDMVD1CardiologicalAnalysisListBoxEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\

    "menuEnt": lambda self,ent:formEntries.menuEnt(self,ent)}
