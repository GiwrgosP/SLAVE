import tika
from tika import parser
import re
import sqlite3

def conn():
    str = "C:\\Users\\Vostro\\Documents\\GitHub\\SLAVE\\dataBase.db"
    try:
        con = sqlite3.connect(str)
        c = con.cursor()
        return c,con
    except:
        print("Error While Connectiong To DataBase", str)

def getEksetasi(c):
    c.execute("SELECT PDF FROM Eksetasi")
    row = c.fetchall()
    rows = list()
    for i in row:
        rows.append(i[0])
    return rows

def indexDoc(doc,tagList):
    indexList = list()
    stringList = {}
    for tag in tagList:
        try:
            startIndex = doc.index(tag)
        except ValueError:
            pass
        else:
            endIndex = startIndex+len(tag)
            indexList.append((startIndex,endIndex))

    indexList = sorted(indexList, key = lambda x : x[1])
    endIndex = len(doc)

    for i in range(len(indexList)-1,-1,-1):
        stringList[doc[indexList[i][0]:indexList[i][1]]] = doc[indexList[i][1]:endIndex]
        endIndex = indexList[i][0]
    return stringList


catDataList = ("Patient Data",\
"Cardio Canine"\
,"Attached images")

catTitleList = ((),
("M-Mode",\
"Doppler",\
"B-Mode"),\
("Owner name",\
"Animal name",\
"Breed","Age",\
"Gender",\
"Weight",\
"Exam Date",\
"Report Data"))

subCatList = (("Aorta/LA","Sphericity Index","EF A-L", "EF SP (Simpson)","EF MOD"),\
("Aorta","MV","MR","Pulmonary A","AVA (VTI)",\
"Pulmonary Capillary Wedge Pressure"),\
("MV","Left Ventricle"))


c,con = conn()
tags = getEksetasi(c)
parsed = parser.from_file('C:\\Users\\Vostro\\Documents\\GitHub\\SLAVE\\Report1.pdf')
metaData = parsed["metadata"]
doc = parsed["content"]
doc = re.sub("\n", " ", doc)
catData = indexDoc(doc,catDataList)

titleData = {}
j = 0
for i in catData:
    data = indexDoc(catData[i],catTitleList[j])
    j+=1
    titleData[i] = data
j = 0
temp = {}
for i in titleData["Cardio Canine"]:
    temp[i] = indexDoc(titleData["Cardio Canine"][i],subCatList[j])
    j+=1


tempTitles = {}
for i in temp:
    tempTitles[i] = {}
    for j in temp[i]:
        tempTitles[i][j] = indexDoc(temp[i][j],tags)

print(tempTitles)
