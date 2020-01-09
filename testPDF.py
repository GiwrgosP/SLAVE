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

print(doc)
