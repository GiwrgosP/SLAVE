import tika
from tika import parser
import db as db
import re
result = {}
tags = db.getEksetasi('C:\\Python37-64\\sof\\SLAVE')

parsed = parser.from_file('C:\\Python37-64\\sof\\SLAVE\\pdf.pdf')

doc = parsed["content"].split("Status:")
doc = doc[0].split("M\xadMode")
doc = re.sub("\n", " ", doc[1])
doc = doc.split(" ")

for tag in tags:
    for i in range(len(doc)):
        print(tag[0],doc[i])
        if str(tag[0]) == str(doc[i]):
            temp = list()
            for j in range(1,tag[2]+1):
                temp.append(doc[i+j])
            result[tag[1]] = temp
            break
print(doc)
print(result)
