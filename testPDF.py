import tika
from tika import parser
import sof as db
import re

from tkinter import filedialog


tags = db.getEksetasi()

parsed = parser.from_file('C:\\Users\\SKPar\\Desktop\\Report.pdf')

tempDoc = parsed["content"].split("Cardio Canine")

tempDoc = tempDoc[0].split("M\xadMode")
tempDoc = re.sub("\n", " ", tempDoc[1])
tempDoc = tempDoc.split(" ")
doc = list()
for i in tempDoc:
    doc.append(re.sub("\xa0", " ", i))
for tag in tags:
    for i in range(len(doc)):
        print(tag[0],doc[i])
        if tag[0] == doc[i]:
            temp = list()
            for j in range(1,tag[2]+1):
                temp.append(re.sub("\xad", "-",doc[i+j]))
            result[tag[0]] = temp
            break
print(doc)
print(result)
