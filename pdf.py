import tika
from tika import parser
import re


tagList = {"Owner name":"",}

parsed = parser.from_file('C:\\Users\\SKPar\\Desktop\\Report.pdf')

doc = parsed["content"]
tempDoc = parsed["content"].split("Owner name")
print(tempDoc)
