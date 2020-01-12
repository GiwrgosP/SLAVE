import tika
from tika import parser
import db as db
import re

from tkinter import filedialog

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    
UploadAction()
result = {}
tags = db.getEksetasi('C:\\Python37-64\\sof\\SLAVE')

parsed = parser.from_file('C:\\Python37-64\\sof\\SLAVE\\pdf.pdf')

tempDoc = parsed["content"].split("Status:")

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
