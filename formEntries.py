import tkinter as tk
import db as db
from tkinter import filedialog
import tika
from tika import parser
import re
from decimal import *

def frameBgColor(ent):
    if ent == 0:
        return "sky blue"
    else:
        temp = ent % 2
        if temp == 0:
            return "sky blue"
        else:
            return "light cyan"

def buildNumber(num, formWindow):
    if num % 1 == 0:
        num = str(int(num))
    else:
        if num % 0.1 == 0:
            num = round(num,1)
        num = str(num)
        if formWindow.master.fileSelected[-2] == "greek":
            num = num.replace(".",",")
    return num

class breedMenuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.pet = self.master.master.fileSelected[-1]
        if self.pet == "dog":
            self.field = ent[0]
        elif self.pet == "cat":
            self.field = 199
        self.values = db.getFieldValues(self.field,self.master.master.path)
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value =  tk.StringVar("")

        menuWidget =  tk.Menubutton(self.mainWidgetFrame, text = self.text)
        self.widgets.append(menuWidget)
        self.applyValues()

        menuEntry = tk.Entry(self.mainWidgetFrame, text = self.value)
        self.widgets.append(menuEntry)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def applyValues(self):
        self.widgets[0].menu =   tk.Menu(self.widgets[0])
        self.widgets[0]["menu"] = self.widgets[0].menu
        for val in self.values:
            self.widgets[0].menu.add_radiobutton(label = val[0], value = val[0],variable = self.value)

    def checkSelf(self):
        flagFound = False
        value = self.value.get()
        for ent in self.values:
            if value == ent[0]:
                flagFound = True
                break
        if flagFound == False:
            db.createFieldValue(self.master.master.path,value,self.field)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        if self.value.get() == "":
            return None
        else:
            self.checkSelf()
            return self.value.get()

class historyMenuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.frames = list()
        self.values = db.getFieldValues(self.field,self.master.master.path)
        self.value = list()
        self.widgets = list()

        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1, sticky = "we", padx = 5, pady = 5)

    def createWidgets(self):
        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)

        tempList = list()

        addButton = tk.Button(widgetFrame, text = "+", command = self.createWidgets)
        destroyButton = tk.Button(widgetFrame, text = "-", command = lambda x = widgetFrame: self.destroyButtonAction(x))
        tempList.append(addButton)
        tempList.append(destroyButton)

        self.value.append(tk.StringVar(value = "+++"))

        menuWidget = tk.Menubutton(widgetFrame, text = self.text)
        menuWidget.menu = tk.Menu(menuWidget)
        menuWidget["menu"] = menuWidget.menu

        for val in self.values:
            menuWidget.menu.add_radiobutton(label = val[0], value = val[0],variable = self.value[-1])

        tempList.append(menuWidget)

        entryWidget = tk.Entry(widgetFrame, width = 120 ,textvariable = self.value[-1])

        tempList.append(entryWidget)

        self.widgets.append(tempList)

        self.gridWidgets()
        widgetFrame.grid(column = 0, row = len(self.frames)-1)

    def gridWidgets(self):
        for frame in self.widgets:
            column = 0
            for ent in frame:
                ent.grid(column = column, row = 0)
                column += 1

    def destroyButtonAction(self,frameForDel):
        if len(self.frames) == 1:
            print("no more frames available for delete")
        else:
            counter = 0
            for frame in self.frames:
                if frame == frameForDel:
                    break
                else:
                    counter += 1

            self.frames[counter].destroy()
            del self.frames[counter]
            del self.value[counter]
            del self.widgets[counter]

    def getWidgetValues(self):
        values = list()
        for ent in self.value:
            val = ent.get()
            if val == "+++" or val == "" :
                pass
            else:
                values.append(val)
        if len(values) == 0:
            return None
        else:
            return values

class dogSASRECardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value = [db.getFieldValues(183,self.master.master.path),\
        db.getFieldValues(196,self.master.master.path)]
        self.values = {"time" : tk.StringVar(value = "+++"),\
        "sas" : tk.StringVar(value = "+++"),\
        "weight" : tk.StringVar(value = "+++"),\
        "age" : tk.StringVar(value = "+++")}

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(widgetLabel)

        menuTime =  tk.Menubutton(self.mainWidgetFrame, text = "Αρ.επισκεψης")
        self.widgets.append(menuTime)
        self.applyValues(1)

        entryTime = tk.Entry(self.mainWidgetFrame, textvariable = self.values["time"])
        self.widgets.append(entryTime)

        menuSas =  tk.Menubutton(self.mainWidgetFrame, text = "sas")
        self.widgets.append(menuSas)
        self.applyValues(3)

        entrySas = tk.Entry(self.mainWidgetFrame, textvariable = self.values["sas"])
        self.widgets.append(entrySas)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1, sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        for i in range(len(self.value)):
            flagFound = False
            if i == 0:
                tag = "time"
            elif i == 1:
                tag = "sas"
            else:
                break
            for j in range(len(self.value[i])):
                if self.value[i][j][0] == self.values[tag].get() or self.values[tag].get() == "+++" :
                    flagFound = True
                    j = len(self.value[i])-1

            if flagFound == False:
                if tag == "time":
                    field = 183
                else:
                    field = 196
                db.createFieldValue(self.master.master.path,self.values[tag].get(),field)

    def refreshVar(self):
        self.values["weight"].set(self.master.entries["weight"].giveValues())
        self.values["age"].set(self.master.entries["age"].giveValues())

    def applyValues(self,pos):
        self.widgets[pos].menu = tk.Menu(self.widgets[pos])
        self.widgets[pos]["menu"] = self.widgets[pos].menu

        if pos == 1:
            tag = "time"
            pos2 = 0
        elif pos == 3:
            tag = "sas"
            pos2 = 1

        for val in self.value[pos2]:
            self.widgets[pos].menu.add_radiobutton(label = val[0], value = val[0],variable = self.values[tag])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        self.refreshVar()
        for val in self.values:
            if self.values[val].get() == "+++" or self.values[val].get() == None :
                return None
        self.checkSelf()
        return self.values["time"].get()  +" καρδιολογικός έλεγχος σε " + \
        self.values["weight"].get() + " " + self.values["age"].get() + \
        " σκύλο " + self.values["sas"].get() + "."

class dogPSRECardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value = [db.getFieldValues(183,self.master.master.path),\
        db.getFieldValues(194,self.master.master.path)]
        self.values = {"time" : tk.StringVar(value = "+++"),\
        "ps" : tk.StringVar(value = "+++"),\
        "weight" : tk.StringVar(value = "+++"),\
        "age" : tk.StringVar(value = "+++")}

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(widgetLabel)

        menuTime =  tk.Menubutton(self.mainWidgetFrame, text = "Αρ.επισκεψης")
        self.widgets.append(menuTime)
        self.applyValues(1)

        entryTime = tk.Entry(self.mainWidgetFrame, textvariable = self.values["time"])
        self.widgets.append(entryTime)

        menuPs =  tk.Menubutton(self.mainWidgetFrame, text = "ps")
        self.widgets.append(menuPs)
        self.applyValues(3)

        entryPs = tk.Entry(self.mainWidgetFrame, textvariable = self.values["ps"])
        self.widgets.append(entryPs)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1, sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        for i in range(len(self.value)):
            flagFound = False
            if i == 0:
                tag = "time"
            elif i == 1:
                tag = "ps"
            else:
                break
            for j in range(len(self.value[i])):
                if self.value[i][j][0] == self.values[tag].get() or self.values[tag].get() == "+++" :
                    flagFound = True
                    j = len(self.value[i])-1

            if flagFound == False:
                if tag == "time":
                    field = 183
                else:
                    field = 194
                db.createFieldValue(self.master.master.path,self.values[tag].get(),field)

    def refreshVar(self):
        self.values["weight"].set(self.master.entries["weight"].giveValues())
        self.values["age"].set(self.master.entries["age"].giveValues())

    def applyValues(self,pos):
        self.widgets[pos].menu = tk.Menu(self.widgets[pos])
        self.widgets[pos]["menu"] = self.widgets[pos].menu

        if pos == 1:
            tag = "time"
            pos2 = 0
        elif pos == 3:
            tag = "ps"
            pos2 = 1

        for val in self.value[pos2]:
            self.widgets[pos].menu.add_radiobutton(label = val[0], value = val[0],variable = self.values[tag])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        self.refreshVar()
        for val in self.values:
            if self.values[val].get() == "+++" or self.values[val].get() == None :
                return None
        self.checkSelf()
        return self.values["time"].get()  +" καρδιολογικός έλεγχος σε " + \
        self.values["weight"].get() + " " + self.values["age"].get() + \
        " σκύλο " + self.values["ps"].get() + "."

class dogPHRECardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value = [db.getFieldValues(183,self.master.master.path),\
        db.getFieldValues(55,self.master.master.path)]
        self.values = {"time" : tk.StringVar(value = "+++"),\
        "hypertension" : tk.StringVar(value = "+++"),\
        "pg" : tk.StringVar(value = "+++"),\
        "weight" : tk.StringVar(value = "+++"),\
        "age" : tk.StringVar(value = "+++")}

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(widgetLabel)

        menuTime =  tk.Menubutton(self.mainWidgetFrame, text = "Αρ.επισκεψης")
        self.widgets.append(menuTime)
        self.applyValues(1)

        entryTime = tk.Entry(self.mainWidgetFrame, textvariable = self.values["time"])
        self.widgets.append(entryTime)

        menuEffusion =  tk.Menubutton(self.mainWidgetFrame, text = "hypertension")
        self.widgets.append(menuEffusion)
        self.applyValues(3)

        entryEffusion = tk.Entry(self.mainWidgetFrame, textvariable = self.values["hypertension"])
        self.widgets.append(entryEffusion)

        spinBoxPg = tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.2f", command = lambda: self.values["pg"].set(str(spinBoxPg.get())))
        self.widgets.append(spinBoxPg)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1, sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        for i in range(len(self.value)):
            flagFound = False
            if i == 0:
                tag = "time"
            elif i == 1:
                tag = "hypertension"
            else:
                break
            for j in range(len(self.value[i])):
                if self.value[i][j][0] == self.values[tag].get() or self.values[tag].get() == "+++" :
                    flagFound = True
                    j = len(self.value[i])-1

            if flagFound == False:
                if tag == "time":
                    field = 183
                else:
                    field = 55
                db.createFieldValue(self.master.master.path,self.values[tag].get(),field)

    def refreshVar(self):
        self.values["weight"].set(self.master.entries["weight"].giveValues())
        self.values["age"].set(self.master.entries["age"].giveValues())

    def applyValues(self,pos):
        self.widgets[pos].menu = tk.Menu(self.widgets[pos])
        self.widgets[pos]["menu"] = self.widgets[pos].menu

        if pos == 1:
            tag = "time"
            pos2 = 0
        elif pos == 3:
            tag = "hypertension"
            pos2 = 1

        for val in self.value[pos2]:
            self.widgets[pos].menu.add_radiobutton(label = val[0], value = val[0],variable = self.values[tag])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        self.refreshVar()
        for val in self.values:
            if self.values[val].get() == "+++" or self.values[val].get() == None :
                return None
        self.checkSelf()
        pgNum = buildNumber(float(self.values["pg"].get()),self.master)
        if pgNum == "0":
            pgNum = "-"
        return self.values["time"].get()  +" καρδιολογικός έλεγχος σε " + \
        self.values["weight"].get() + " " + self.values["age"].get() + \
        " σκύλο " + self.values["hypertension"].get() +"(PG: " + pgNum +" mmHg)."

class catHOCMREardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value = [db.getFieldValues(183,self.master.master.path),\
        db.getFieldValues(191,self.master.master.path)]
        self.values = {"time" : tk.StringVar(value = "+++"),\
        "hocm" : tk.StringVar(value = "+++"),\
        "weight" : tk.StringVar(value = "+++"),\
        "age" : tk.StringVar(value = "+++")}

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(widgetLabel)

        menuTime =  tk.Menubutton(self.mainWidgetFrame, text = "Αρ.επισκεψης")
        self.widgets.append(menuTime)
        self.applyValues(1)

        entryTime = tk.Entry(self.mainWidgetFrame, textvariable = self.values["time"])
        self.widgets.append(entryTime)

        menuDcm =  tk.Menubutton(self.mainWidgetFrame, text = "hocm")
        self.widgets.append(menuDcm)
        self.applyValues(3)

        entryDmc = tk.Entry(self.mainWidgetFrame, textvariable = self.values["hocm"])
        self.widgets.append(entryDmc)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        for i in range(len(self.value)):
            flagFound = False
            if i == 0:
                tag = "time"
            elif i == 1:
                tag = "hocm"
            for j in range(len(self.value[i])):
                if self.value[i][j][0] == self.values[tag].get() or self.values[tag].get() == "+++" :
                    flagFound = True
                    j = len(self.value[i])-1

            if flagFound == False:
                if tag == "time":
                    field = 183
                elif tag == "hocm":
                    field = 191
                db.createFieldValue(self.master.master.path,self.values[tag].get(),field)

    def refreshVar(self):
        self.values["weight"].set(self.master.entries["weight"].giveValues())
        self.values["age"].set(self.master.entries["age"].giveValues())

    def applyValues(self,pos):
        self.widgets[pos].menu = tk.Menu(self.widgets[pos])
        self.widgets[pos]["menu"] = self.widgets[pos].menu

        if pos == 1:
            tag = "time"
            pos2 = 0
        elif pos == 3:
            tag = "hocm"
            pos2 = 1
        for val in self.value[pos2]:
            self.widgets[pos].menu.add_radiobutton(label = val[0], value = val[0],variable = self.values[tag])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        self.refreshVar()
        for val in self.values:
            if self.values[val].get() == "+++" or self.values[val].get() == None :
                return None
        self.checkSelf()
        return self.values["time"].get()  +" καρδιολογικός έλεγχος σε " + \
        self.values["weight"].get() + " " + self.values["age"].get() + \
        " "+self.values["hocm"].get() + "."

class catHCMRECardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value = [db.getFieldValues(183,self.master.master.path),\
        db.getFieldValues(188,self.master.master.path),\
        db.getFieldValues(185,self.master.master.path),\
        db.getFieldValues(186,self.master.master.path)]
        self.values = {"time" : tk.StringVar(value = "+++"),\
        "hcm" : tk.StringVar(value = "+++"),\
        "cardFail" : tk.StringVar(value = "+++"),\
        "effusion" : tk.StringVar(value = "+++"),\
        "weight" : tk.StringVar(value = "+++"),\
        "age" : tk.StringVar(value = "+++")}

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(widgetLabel)

        menuTime =  tk.Menubutton(self.mainWidgetFrame, text = "Αρ.επισκεψης")
        self.widgets.append(menuTime)
        self.applyValues(1)

        entryTime = tk.Entry(self.mainWidgetFrame, textvariable = self.values["time"])
        self.widgets.append(entryTime)

        menuDcm =  tk.Menubutton(self.mainWidgetFrame, text = "hcm")
        self.widgets.append(menuDcm)
        self.applyValues(3)

        entryDmc = tk.Entry(self.mainWidgetFrame, textvariable = self.values["hcm"])
        self.widgets.append(entryDmc)

        menuCardFail =  tk.Menubutton(self.mainWidgetFrame, text = "cardFail")
        self.widgets.append(menuCardFail)
        self.applyValues(5)

        entryCardFail = tk.Entry(self.mainWidgetFrame, textvariable = self.values["cardFail"])
        self.widgets.append(entryCardFail)

        menuEffusion =  tk.Menubutton(self.mainWidgetFrame, text = "effusion")
        self.widgets.append(menuEffusion)
        self.applyValues(7)

        entryEffusion = tk.Entry(self.mainWidgetFrame, textvariable = self.values["effusion"])
        self.widgets.append(entryEffusion)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        for i in range(len(self.value)):
            flagFound = False
            if i == 0:
                tag = "time"
            elif i == 1:
                tag = "hcm"
            elif i == 2:
                tag = "cardFail"
            else:
                tag = "effusion"
            for j in range(len(self.value[i])):
                if self.value[i][j][0] == self.values[tag].get() or self.values[tag].get() == "+++" :
                    flagFound = True
                    j = len(self.value[i])-1

            if flagFound == False:
                if tag == "time":
                    field = 183
                elif tag == "hcm":
                    field = 188
                elif tag == "cardFail":
                    field = 185
                elif tag == "effusion":
                        field = 186
                db.createFieldValue(self.master.master.path,self.values[tag].get(),field)

    def refreshVar(self):
        self.values["weight"].set(self.master.entries["weight"].giveValues())
        self.values["age"].set(self.master.entries["age"].giveValues())

    def applyValues(self,pos):
        self.widgets[pos].menu = tk.Menu(self.widgets[pos])
        self.widgets[pos]["menu"] = self.widgets[pos].menu

        if pos == 1:
            tag = "time"
            pos2 = 0
        elif pos == 3:
            tag = "hcm"
            pos2 = 1
        elif pos == 5:
            tag = "cardFail"
            pos2 = 2
        else:
            tag = "effusion"
            pos2 = 3

        for val in self.value[pos2]:
            self.widgets[pos].menu.add_radiobutton(label = val[0], value = val[0],variable = self.values[tag])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        self.refreshVar()
        for val in self.values:
            if self.values[val].get() == "+++" or self.values[val].get() == None :
                return None
        self.checkSelf()
        return self.values["time"].get()  +" καρδιολογικός έλεγχος σε " + \
        self.values["weight"].get() + " " + self.values["age"].get() + \
        " με "+self.values["hcm"].get() + " και " +\
        self.values["cardFail"].get() + " " + self.values["effusion"].get() + "."

class dogPERECardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value = [db.getFieldValues(183,self.master.master.path),\
        db.getFieldValues(186,self.master.master.path)]
        self.values = {"time" : tk.StringVar(value = "+++"),\
        "effusion" : tk.StringVar(value = "+++"),\
        "weight" : tk.StringVar(value = "+++"),\
        "age" : tk.StringVar(value = "+++")}

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(widgetLabel)

        menuTime =  tk.Menubutton(self.mainWidgetFrame, text = "Αρ.επισκεψης")
        self.widgets.append(menuTime)
        self.applyValues(1)

        entryTime = tk.Entry(self.mainWidgetFrame, textvariable = self.values["time"])
        self.widgets.append(entryTime)

        menuEffusion =  tk.Menubutton(self.mainWidgetFrame, text = "effusion")
        self.widgets.append(menuEffusion)
        self.applyValues(3)

        entryEffusion = tk.Entry(self.mainWidgetFrame, textvariable = self.values["effusion"])
        self.widgets.append(entryEffusion)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        for i in range(len(self.value)):
            flagFound = False
            if i == 0:
                tag = "time"
            elif i == 1:
                tag = "effusion"
            for j in range(len(self.value[i])):
                if self.value[i][j][0] == self.values[tag].get() or self.values[tag].get() == "+++" :
                    flagFound = True
                    j = len(self.menuValues[i])-1

            if flagFound == False:
                if tag == "time":
                    field = 183
                else:
                    field = 184
                db.createFieldValue(self.master.master.path,self.values[tag].get(),field)

    def refreshVar(self):
        self.values["weight"].set(self.master.entries["weight"].giveValues())
        self.values["age"].set(self.master.entries["age"].giveValues())

    def applyValues(self,pos):
        self.widgets[pos].menu = tk.Menu(self.widgets[pos])
        self.widgets[pos]["menu"] = self.widgets[pos].menu

        if pos == 1:
            tag = "time"
            pos2 = 0
        elif pos == 3:
            tag = "effusion"
            pos2 = 1

        for val in self.value[pos2]:
            self.widgets[pos].menu.add_radiobutton(label = val[0], value = val[0],variable = self.values[tag])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        self.refreshVar()
        for val in self.values:
            if self.values[val].get() == "+++" or self.values[val].get() == None :
                return None
        self.checkSelf()
        return self.values["time"].get()  +" καρδιολογικός έλεγχος σε " + \
        self.values["weight"].get() + " " + self.values["age"].get() + \
        " " + self.values["effusion"].get() + "."

class dogDCMRECardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value = [db.getFieldValues(183,self.master.master.path),\
        db.getFieldValues(184,self.master.master.path),\
        db.getFieldValues(185,self.master.master.path),\
        db.getFieldValues(186,self.master.master.path)]
        self.values = {"time" : tk.StringVar(value = "+++"),\
        "dcm" : tk.StringVar(value = "+++"),\
        "cardFail" : tk.StringVar(value = "+++"),\
        "effusion" : tk.StringVar(value = "+++"),\
        "weight" : tk.StringVar(value = "+++"),\
        "age" : tk.StringVar(value = "+++")}

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(widgetLabel)

        menuTime =  tk.Menubutton(self.mainWidgetFrame, text = "Αρ.επισκεψης")
        self.widgets.append(menuTime)
        self.applyValues(1)

        entryTime = tk.Entry(self.mainWidgetFrame, textvariable = self.values["time"])
        self.widgets.append(entryTime)

        menuDcm =  tk.Menubutton(self.mainWidgetFrame, text = "dcm")
        self.widgets.append(menuDcm)
        self.applyValues(3)

        entryDmc = tk.Entry(self.mainWidgetFrame, textvariable = self.values["dcm"])
        self.widgets.append(entryDmc)

        menuCardFail =  tk.Menubutton(self.mainWidgetFrame, text = "cardFail")
        self.widgets.append(menuCardFail)
        self.applyValues(5)

        entryCardFail = tk.Entry(self.mainWidgetFrame, textvariable = self.values["cardFail"])
        self.widgets.append(entryCardFail)

        menuEffusion =  tk.Menubutton(self.mainWidgetFrame, text = "effusion")
        self.widgets.append(menuEffusion)
        self.applyValues(7)

        entryEffusion = tk.Entry(self.mainWidgetFrame, textvariable = self.values["effusion"])
        self.widgets.append(entryEffusion)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1, sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        for i in range(len(self.value)):
            flagFound = False
            if i == 0:
                tag = "time"
            elif i == 1:
                tag = "dcm"
            elif i == 2:
                tag = "cardFail"
            else:
                tag = "effusion"
            for j in range(len(self.value[i])):
                if self.value[i][j][0] == self.values[tag].get() or self.values[tag].get() == "+++" :
                    flagFound = True
                    j = len(self.menuValues[i])-1

            if flagFound == False:
                field = 183+i
                db.createFieldValue(self.master.master.path,self.values[tag].get(),field)

    def refreshVar(self):
        self.values["weight"].set(self.master.entries["weight"].giveValues())
        self.values["age"].set(self.master.entries["age"].giveValues())

    def applyValues(self,pos):
        self.widgets[pos].menu = tk.Menu(self.widgets[pos])
        self.widgets[pos]["menu"] = self.widgets[pos].menu

        if pos == 1:
            tag = "time"
            pos2 = 0
        elif pos == 3:
            tag = "dcm"
            pos2 = 1
        elif pos == 5:
            tag = "cardFail"
            pos2 = 2
        else:
            tag = "effusion"
            pos2 = 3

        for val in self.value[pos2]:
            self.widgets[pos].menu.add_radiobutton(label = val[0], value = val[0],variable = self.values[tag])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        self.refreshVar()
        for val in self.values:
            if self.values[val].get() == "+++" or self.values[val].get() == None :
                return None
        self.checkSelf()
        return self.values["time"].get()  +" καρδιολογικός έλεγχος σε " + \
        self.values["weight"].get() + " " + self.values["age"].get() + \
        " σκύλο "+self.values["dcm"].get() + \
        self.values["cardFail"].get() + " " + self.values["effusion"].get() + "."

class dogDMVD1CardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.weightAgeValues = {"weight" : tk.StringVar(value = "+++"), "age" : tk.StringVar(value = "+++"), "currentValue" : tk.StringVar(value = "")}

        menuWidget =  tk.Menubutton(self.mainWidgetFrame, text = self.text)
        self.widgets.append(menuWidget)

        buttom = tk.Button(self.mainWidgetFrame, text = "Populatee", command = self.buttonAction)
        self.widgets.append(buttom)

        self.applyValues()
        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def buttonAction(self):
        self.refreshVar()

    def applyValues(self):
        self.values = ("Καρδιολογικός έλεγχος σε "+self.weightAgeValues["weight"].get()+" "+self.weightAgeValues["age"].get()+" σκύλο με υποψία καρδιακής νόσου.",\
                    "Προεγχειρητικός καρδιολογικός έλεγχος σε "+self.weightAgeValues["weight"].get()+" "+self.weightAgeValues["age"].get()+" σκύλο.",\
                    "Προληπτικός καρδιολογικός έλεγχος σε "+self.weightAgeValues["weight"].get()+" "+self.weightAgeValues["age"].get()+" σκύλο.",\
                    "Προεγχειρητικός και προληπτικός  καρδιολογικός έλεγχος σε "+self.weightAgeValues["weight"].get()+" "+self.weightAgeValues["age"].get()+" σκύλο.")
        self.widgets[0].menu =   tk.Menu(self.widgets[0])
        self.widgets[0]["menu"] = self.widgets[0].menu
        for val in self.values:
            self.widgets[0].menu.add_radiobutton(label = val, value = val,variable = self.weightAgeValues["currentValue"])

    def refreshVar(self):
        self.weightAgeValues["weight"].set(self.master.entries["weight"].giveValues())
        self.weightAgeValues["age"].set(self.master.entries["age"].giveValues())
        self.applyValues()

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = self.weightAgeValues["currentValue"].get()
        if input == "":
            return None
        return input

class dogDMVD1RECardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value = [db.getFieldValues(183,self.master.master.path),\
        db.getFieldValues(197,self.master.master.path),\
        db.getFieldValues(57,self.master.master.path)]
        self.values = {"weight" : tk.StringVar(value = "+++"),\
        "age" : tk.StringVar(value = "+++"),\
        "time" : tk.StringVar(value = "+++"),\
        "yG" : tk.StringVar(value = "+++"),\
        "clinicalstage" : tk.StringVar(value = "+++")}

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(widgetLabel)

        menuTime = tk.Menubutton(self.mainWidgetFrame, text = "Αρ. επισκεψης" )
        self.widgets.append(menuTime)
        self.applyValues(1)

        menuYg =  tk.Menubutton(self.mainWidgetFrame, text = "Υ/Γ")
        self.widgets.append(menuYg)
        self.applyValues(2)

        menuClinicalState = tk.Menubutton(self.mainWidgetFrame, text = "Κλινικό στάδιο")
        self.widgets.append(menuClinicalState)
        self.applyValues(3)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def refreshVar(self):
        self.values["weight"].set(self.master.entries["weight"].giveValues())
        self.values["age"].set(self.master.entries["age"].giveValues())

    def applyValues(self,pos):
        self.widgets[pos].menu = tk.Menu(self.widgets[pos])
        self.widgets[pos]["menu"] = self.widgets[pos].menu
        for val in self.value[pos-1]:
            if pos == 1:
                self.widgets[pos].menu.add_radiobutton(label = val[0], value = val[0],variable = self.values["time"])
            elif pos == 2:
                self.widgets[pos].menu.add_radiobutton(label = val[0], value = val[0],variable = self.values["yG"])
            else:
                self.widgets[pos].menu.add_radiobutton(label = val[0], value = val[0],variable = self.values["clinicalstage"])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        self.refreshVar()
        for val in self.values:
            if self.values[val].get() == "+++" or self.values[val].get() == None :
                return None
        return self.values["time"].get()  +" καρδιολογικός έλεγχος σε " + \
        self.values["weight"].get() + " " + self.values["age"].get() + \
        " σκύλο με εκφυλιστική νόσο της μιτροειδούς βαλβίδας "+self.values["yG"].get() + \
        " Υ/Γ σταδίου – " + self.values["clinicalstage"].get() + " κλινικού σταδίου (ACVIM Consensus 2019)."

class auditoryFindingsMenuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.values = [db.getFieldValues(201,self.master.master.path),\
        db.getFieldValues(202,self.master.master.path),\
        db.getFieldValues(203,self.master.master.path),\
        db.getFieldValues(204,self.master.master.path),
        db.getFieldValues(205,self.master.master.path),\
        db.getFieldValues(206,self.master.master.path)]

        self.value = list()

        self.widgets = list()

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text )
        self.widgets.append(widgetLabel)

        systolicMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "systolic")
        self.applyValues(systolicMenuWidget,0)
        self.widgets.append(systolicMenuWidget)

        degreeMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "degree")
        self.applyValues(degreeMenuWidget,1)
        self.widgets.append(degreeMenuWidget)

        ausculationMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "ausculation")
        self.applyValues(ausculationMenuWidget,2)
        self.widgets.append(ausculationMenuWidget)

        auditoryMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "auditory")
        self.applyValues(auditoryMenuWidget,3)
        self.widgets.append(auditoryMenuWidget)

        heartMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "heart")
        self.applyValues(heartMenuWidget,4)
        self.widgets.append(heartMenuWidget)

        valveMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "valve")
        self.applyValues(valveMenuWidget,5)
        self.widgets.append(valveMenuWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def getWidgetValues(self):
        input = list()
        for val in self.value:
            temp = val.get()
            if temp != "":
                input.append(temp)
            else:
                return None
        return input[0] + ", " + input[1] + ", " + input[2] + \
        ", με σημείο αποκλειστικής ακροασιμότητας στο " + input[3] + \
        " ημιθωράκιο, στην " + input[4] + " της καρδιάς, στο ύψος της " \
        + input[5] + " βαλβίδας."

    def applyValues(self,widget,pos):
        self.value.append(tk.StringVar(value = "+++"))
        widget.menu = tk.Menu(widget)
        widget["menu"] = widget.menu

        widget.menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[-1])

        for val in self.values[pos]:
                widget.menu.add_radiobutton(label = val[0], value = val[0],variable = self.value[-1])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

class weightSpinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.pet = self.master.master.fileSelected[-1]

        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()

        spinBoxLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(spinBoxLabel)

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f", command = lambda: self.giveValues())
        self.widgets.append(spinBoxWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def giveValues(self):
        val = float(self.widgets[1].get())
        if self.pet == "dog":
            if val == 0.0:
                return "+++"
            elif val <= 15.00:
                return "μικρόσωμο"
            elif val <= 55.00:
                return "μεγαλόσωμο"
            else:
                return "γιαγαντόσωμο"
        elif self.pet == "cat":
            if val == 0.0:
                return "+++"
            elif val <= 15.00:
                return "μικρόσωμο"
            elif val <= 55.00:
                return "μεγαλόσωμο"
            else:
                return "γιαγαντόσωμο"
        else:
            print("PROBLEM WITH PET RACE")


        return "+++"

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = float(self.widgets[1].get())
        if input == 0.0:
            return None
        return buildNumber(input,self.master)

class bodyWeightSpinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()

        spinBoxLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(spinBoxLabel)

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0.0, to = 5, increment=0.5)
        self.widgets.append(spinBoxWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def getWidgetValues(self):
        num = float(self.widgets[1].get())
        if num < 1.5:
            input = "Καχεξία (BS: "
        elif num < 2.5:
            input = "Αδύνατο (BS: "
        elif num <= 4.0:
            input = "Κανονικό σωματικό βάρος (BS: "
        elif num <= 5:
            input = "Παχύσαρκο (BS: "
        else:
            return None

        temp = buildNumber(num, self.master)
        input += temp + "/5)"

        return input

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

class nameAitEntryEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value = tk.StringVar(value = "+++")

        self.master.entries["petName"].widgets[1].bind("<Key>",lambda _: self.callback(self))

        entryLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(entryLabel)

        entryWidget = tk.Entry(self.mainWidgetFrame, textvariable = self.value)
        self.widgets.append(entryWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def callback(event,self):
        petName = self.master.entries["petName"].value["petName"].get()
        self.value.set(petName)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = self.value.get()
        if input == "+++" or input == "":
            return None
        return input

class checkUpSpinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()

        spinBoxLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(spinBoxLabel)

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=1)
        self.widgets.append(spinBoxWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def getWidgetValues(self):
        monthCounter = {
        1:"Ιανουάριος",\
        2:"Φεβρουάριος",\
        3:"Μάρτιος",\
        4:"Απρίλιος",\
        5:"Μάιος",\
        6:"Ιούνιος",\
        7:"Ιούλιος",\
        8:"Αύγουστος",\
        9:"Σεπτέμβριος",\
        10:"Οκτώβριος",\
        11:"Νοέμβριος",\
        12:"Δεκέμβριος"
        }
        input = list()
        curDate = self.master.entries["date"].getWidgetValues()
        if curDate!= None:
            curDate = curDate.split(".")

            curMonth = int(curDate[1])
            curYear = int(curDate[2])
            endDate = int(self.widgets[1].get())

            endMonth = monthCounter[(curMonth + endDate) % 12]
            endYear = (curMonth + endDate) // 12
            endYear+= curYear
            temp = list()
            temp.append(str(endDate))
            temp.append(endMonth)
            temp.append(str(endYear))
            input.append(temp)
        else:
            return None
        return input

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

class flowButtonEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.state = False
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.buttonValue = tk.StringVar(value = "")
        self.widgets = list()

        button = tk.Button(self.mainWidgetFrame, text = self.text, command = self.buttonAction)
        self.widgets.append(button)

        self.gridWidgets()

        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def buttonAction(self):
        self.state = not self.state

        if self.state == True:
            self.buttonValue.set("Αντιστροφή Ε & Α κύματος διαμιτροειδικής ροής, εύρημα συμβατό με  1ου βαθμού διαστολική δυσλειτουργία του μυοκαρδίου.")
            self.widgets[0].configure(bg = "red")
        else:
            self.buttonValue.set("")
            self.widgets[0].configure(bg = "white")

    def getWidgetValues(self):
        input = self.buttonValue.get()
        if input == "":
            return None
        return input

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

class ecgMenuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.frames = list()
        self.values = db.getFieldValues(self.field,self.master.master.path)
        self.value = list()
        self.widgets = list()

        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def createWidgets(self):
        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)

        addButton = tk.Button(widgetFrame, text = "+", command = self.createWidgets)
        destroyButton = tk.Button(widgetFrame, text = "-", command = lambda x = widgetFrame: self.destroyButtonAction(x))

        menuWidget = tk.Menubutton(widgetFrame, text = self.text)
        menuWidget.menu = tk.Menu(menuWidget)
        menuWidget["menu"] = menuWidget.menu

        self.value.append(tk.StringVar(value = ""))

        for val in self.values:
            menuWidget.menu.add_radiobutton(label = val[0], value = val[0],variable = self.value[-1])

        menuEntry = tk.Entry(widgetFrame, text = self.value[-1])

        tempListWidgets = list()
        tempListWidgetsInput = list()

        tempListWidgets.append(addButton)
        tempListWidgets.append(destroyButton)

        tempListWidgets.append(menuWidget)

        tempListWidgets.append(menuEntry)

        self.widgets.append(tempListWidgets)

        self.gridWidgets()
        widgetFrame.grid(column = 0, row = len(self.frames)-1)

    def gridWidgets(self):
        for frame in self.widgets:
            column = 0
            for ent in frame:
                ent.grid(column = column, row = 0)
                column += 1

    def destroyButtonAction(self,frameForDel):
        if len(self.frames) == 1:
            print("no more frames available for delete")
        else:
            counter = 0
            for frame in self.frames:
                if frame == frameForDel:
                    break
                else:
                    counter += 1

            self.frames[counter].destroy()
            del self.frames[counter]
            del self.value[counter]
            del self.widgets[counter]

    def getWidgetValues(self):
        values = list()
        for ent in self.value:
            val = ent.get()
            if val == "":
                pass
            else:
                values.append(val)

        self.checkSelf()
        if len(values) == 0:
            return None
        else:
            return values

    def checkSelf(self):

        for val in self.value:
            flagFound = False
            for k in self.values:
                if k[0] == val.get():
                    flagFound = True
                    break
            if flagFound == False:
                db.createFieldValue(self.master.master.path,val.get(),self.field)

class ageSpinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.pet = self.master.master.fileSelected[-1]
        self.value = tk.IntVar()
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()

        spinBoxLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(spinBoxLabel)

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=1)
        self.widgets.append(spinBoxWidget)

        radioButton1 = tk.Radiobutton(self.mainWidgetFrame, variable = self.value, text="Μηνών", value=1)
        self.widgets.append(radioButton1)

        radioButton2 = tk.Radiobutton(self.mainWidgetFrame ,variable = self.value, text="Ετών", value=2)
        radioButton2.select()
        self.widgets.append(radioButton2)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)


    def giveValues(self):
        num = int(self.widgets[1].get())
        approx = self.value.get()

        if  num == 0:
            return "+++"
        else:
            if self.pet == "dog":
                if approx == 1:
                    return "νεαρό"
                else:
                    if num< 4:
                        return "νεαρό"
                    elif num < 8:
                        return "ενήλικο"
                    else:
                        return "υπερήλικο"
            elif self.pet == "cat":
                if approx == 1:
                    return "νεαρό"
                else:
                    if num<= 2:
                        return "νεαρό"
                    elif num <= 3:
                        return "ενήλικο"
                    else:
                        return "υπερήλικο"
            else:
                print("PROBLEM WITH PET RACE")

        return "+++"

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        age = int(self.widgets[1].get())
        timeAproximation = self.value.get()

        flagPlural = True
        if age == 0:
            return None
        if age <= 1:
            flagPlural = False

        if timeAproximation == 2:
            textTimeAproximation = " ετών"
            if flagPlural == False:
                textTimeAproximation = " έτους"
        else:
            textTimeAproximation = " μηνών"
            if flagPlural == False:
                textTimeAproximation = " μηνός"

        return str(age)+textTimeAproximation


class medicMenuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.frames = list()
        self.value = list()
        self.values = list()
        self.widgets = list()

        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def createWidgets(self):
        tempListWidgets = list()
        tempListValue = list()
        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)

        addButton = tk.Button(widgetFrame, text = "+", command = self.createWidgets)
        destroyButton = tk.Button(widgetFrame, text = "-", command = lambda x = widgetFrame: self.destroyButtonAction(x))

        tempListWidgets.append(addButton)
        tempListWidgets.append(destroyButton)

        menuWidget = tk.Menubutton(widgetFrame, text = self.text)
        tempListValue.append(self.applyValues(self.field,menuWidget))
        tempListWidgets.append(menuWidget)

        menuEntry = tk.Entry(widgetFrame, textvariable = tempListValue[-1])
        tempListWidgets.append(menuEntry)


        tempListValue.append(tk.StringVar())
        spinBoxWidget = tk.Spinbox(widgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f",textvariable = tempListValue[-1])
        tempListWidgets.append(spinBoxWidget)

        menuWidget = tk.Menubutton(widgetFrame, text = "Μονάδα μέτρησης")
        tempListValue.append(self.applyValues(25,menuWidget))
        tempListWidgets.append(menuWidget)

        menuWidget = tk.Menubutton(widgetFrame, text = "Δοσολογία")
        tempListValue.append(self.applyValues(26,menuWidget))
        tempListWidgets.append(menuWidget)

        menuEntry = tk.Entry(widgetFrame, text = tempListValue[-1])
        tempListWidgets.append(menuEntry)

        self.widgets.append(tempListWidgets)
        self.value.append(tempListValue)

        self.gridWidgets()
        widgetFrame.grid(column = 0, row = len(self.widgets)-1)

    def applyValues(self,field,menuWidget):
        values = db.getFieldValues(field,self.master.master.path)
        self.values.append(values)
        k = tk.StringVar(value = "")

        menuWidget.menu = tk.Menu(menuWidget)
        menuWidget["menu"] = menuWidget.menu

        for val in values:
            menuWidget.menu.add_radiobutton(label = val[0], value = val[0],variable = k)
        return k

    def gridWidgets(self):
        for frame in self.widgets:
            column = 0
            for ent in frame:
                ent.grid(column = column, row = 0)
                column += 1

    def destroyButtonAction(self,frameForDel):
        if len(self.frames) == 1:
            print("no more frames available for delete")
        else:
            counter = 0
            for frame in self.frames:
                if frame == frameForDel:
                    break
                else:
                    counter += 1

            self.frames[counter].destroy()
            del self.frames[counter]
            del self.value[counter]
            del self.widgets[counter]

    def getWidgetValues(self):
        values = list()
        for frame in self.value:
            input = frame[0].get()
            if input != "":
                num = buildNumber(float(frame[1].get()),self.master)
                values.append([input," (" + num + " " + frame[2].get()+ " " + frame[3].get() + "), "])
            else:
                pass

        if len(values) != 0:
            values[-1][1] = values[-1][1][:-2]
            self.checkSelf()
            return values
        else:
            return None

    def checkSelf(self):
        for frame in self.value:
            for i in range(len(frame)-1):
                if i == 1:
                    pass
                else:
                    j = i
                    if i != 0:
                        j -= 1
                    flagFound = False
                    for val in self.values[j]:
                        if val[0] == frame[i].get():
                            flagFound = True
                            break
                    if flagFound == False:
                        if i == 0:
                            field = self.field
                        elif i == 2:
                            field = 25
                        elif i == 3:
                            field = 26
                        else:
                            print("error with field")
                        print(frame[i],field)
                        db.createFieldValue(self.master.master.path,frame[i].get(),field)

class pdfReader(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.currentValue =  tk.StringVar(value = "+++")
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()

        button = tk.Button(self.mainWidgetFrame, text = self.text, command = self.buttonAction)
        self.widgets.append(button)

        buttonEntry = tk.Entry(self.mainWidgetFrame, text = self.currentValue, state = 'disabled' )
        self.widgets.append(buttonEntry)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def buttonAction(self):
        fileName = filedialog.askopenfilename(filetypes = (("pdf files","*.pdf"),))
        self.currentValue.set(fileName)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        fileName = self.currentValue.get()
        if fileName == "+++":
            return None
        else:
            tags = db.getEksetasi(self.master.master.path)
            parsed = parser.from_file(fileName)
            tempDoc = parsed["content"].split("Status:")
            tempDoc = tempDoc[0].split("M\xadMode")
            tempDoc = re.sub("\n", " ", tempDoc[1])
            tempDoc = tempDoc.split(" ")
            doc = list()
            result = {}
            for i in tempDoc:
                doc.append(re.sub("\xa0", " ", i))
            for tag in tags:
                for i in range(len(doc)):
                    if tag[0] == doc[i]:
                        temp = list()
                        for j in range(1,tag[2]+1):
                            temp.append(re.sub("\xad", "",doc[i+j]))
                        result[tag[1]] = temp
                        break

            input = {}
            for i in result:
                if len(result[i])==2 and result[i][1] == "cm":
                    temp = float(Decimal(result[i][0]) * Decimal(10))
                else:
                    temp = float(result[i][0])

                input[i] = buildNumber(temp,self.master)

        return input

class menuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(ent[5]))
        self.widgets = list()
        self.value =  tk.StringVar(value = "+++")
        self.values = db.getFieldValues(self.field,self.master.master.path)

        menuWidget =  tk.Menubutton(self.mainWidgetFrame, text = self.text)
        self.widgets.append(menuWidget)
        self.applyValues()

        menuEntry = tk.Entry(self.mainWidgetFrame, text = self.value)
        self.widgets.append(menuEntry)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def applyValues(self):
        self.widgets[0].menu =   tk.Menu(self.widgets[0])
        self.widgets[0]["menu"] = self.widgets[0].menu
        for val in self.values:
            self.widgets[0].menu.add_radiobutton(label = val[0], value = val[0],variable = self.value)

    def checkSelf(self):
        flagFound = False
        value = self.value.get()
        for ent in self.values:
            if value == ent[0]:
                flagFound = True
                break
        if flagFound == False:
            db.createFieldValue(self.master.master.path,value,self.field)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        if self.value.get() == "+++" or self.value.get() == "" :
            return None
        else:
            self.checkSelf()
            return self.value.get()

class entryEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.sort = ent[5]
        self.value = { self.name : tk.StringVar(value = "+++")}
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.text, textvariable = self.value[self.name]))
        self.widgets.append(tk.Entry(self.mainWidgetFrame))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = self.value[self.name].get()
        if len(input.split()) == 0 or input == "+++":
            return None
        return input
