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
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.field = db.getWidgetMenus(self.master.master.path,widgetId)
        self.name = name
        self.sort = sort
        self.pet = self.master.master.fileSelected[2]
        self.value =  { self.field[0][2] : tk.StringVar(value = "+++") }
        self.values = { self.field[0][2] : db.getValues(self.master.master.path,self.field[0][0]) }
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Menubutton(self.mainWidgetFrame, text = self.name))
        self.widgets[0].menu =   tk.Menu(self.widgets[0])
        self.widgets[0]["menu"] = self.widgets[0].menu
        self.widgets[0].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[self.field[0][2]])

        for val in self.values[self.field[0][2]]:
            self.widgets[0].menu.add_radiobutton(label = val[0], value = val[0],variable = self.value[self.field[0][2]])

        self.widgets.append(tk.Entry(self.mainWidgetFrame, text = self.value[self.field[0][2]]))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        if self.values[self.field[2]].count(self.value[self.field[0][2]]) == 0:
            db.createValue(self.master.master,self.value[self.field[0][2]],self.field[0][0])

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
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.field = db.getWidgetMenus(self.master.master.path,widgetId)
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.frames = list()
        self.values = {self.field[0][2] : db.getValues(self.master.master.path,self.field[0][0])}
        self.value = {self.field[0][2] : list()}
        self.widgets = list()

        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort, sticky = "we", padx = 5, pady = 5)

    def createWidgets(self):
        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)

        tempList = list()

        tempList.append(tk.Button(widgetFrame, text = "+", command = self.createWidgets))
        tempList.append(tk.Button(widgetFrame, text = "-", command = lambda x = widgetFrame: self.destroyButtonAction(x)))

        self.value[self.field[0][2]].append(tk.StringVar(value = "+++"))

        tempList.append(tk.Menubutton(widgetFrame, text = self.name))
        tempList[-1].menu = tk.Menu(tempList[-1])
        tempList[-1]["menu"] = tempList[-1].menu
        tempList[-1].menu.add_radiobutton(label = "+++", value = "+++", variable = self.value[self.field[0][2]][-1])

        for val in self.values[self.field[0][2]]:
            tempList[-1].menu.add_radiobutton(label = val[0], value = val[0],variable = self.value[self.field[0][2]][-1])

        tempList.append( tk.Entry(widgetFrame, width = 120 ,textvariable = self.value[self.field[0][2]][-1]))


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
            del self.value[self.field[2]][counter]
            del self.widgets[counter]

    def getWidgetValues(self):
        values = list()
        for ent in self.value[self.field[0][2]]:
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
                    "Προεγχειρητικό ς και προληπτικός  καρδιολογικός έλεγχος σε "+self.weightAgeValues["weight"].get()+" "+self.weightAgeValues["age"].get()+" σκύλο.")
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
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.widgetMenus = db.getWidgetMenus(self.master.master.path,widgetId)
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.field = {}
        self.value = {}
        self.values = {}
        for menu in self.widgetMenus:
            self.value [menu[2]] = tk.StringVar(value = "+++")
            self.values [menu[2]] = db.getValues(self.master.master.path,menu[0])
            self.fields [menu[2]] = menu[0]

        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name ))

        for menuId in self.values:
            self.widgets.append(tk.Menubutton(self.mainWidgetFrame, text = menuId ))
            self.widget[-1].menu = tk.Menu(self.widget[-1])
            self.widget[-1]["menu"] = self.widget[-1].menu

            self.widget[-1].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[menuId])
            for val in self.values[menu]:
                self.widget[-1].menu.add_radiobutton(label = val, value = val,variable = self.value[menuId])


        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort ,sticky = "we",padx = 5, pady = 5)

    def getWidgetValues(self):
        flag = True
        for menu in self.value:
            if self.value[menu] == "+++" :
                flag = False
                break

        if flag == True:
            return self.value
        else:
            return None

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

class weightSpinBoxEnt(tk.Tk):
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.name = name
        self.sort = sort
        self.pet = self.master.master.fileSelected[2]
        self.value = {self.name : tk.StringVar(value = "0.0")}
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))

        self.widgets.append(tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f", textvariable = self.value[self.name]))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def giveValues(self):
        val = float(self.value[self.name].get())
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
    def __init__(self, master, name, widgetId,sort):
        self.master = master
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))

        self.widgets.append(tk.Spinbox(self.mainWidgetFrame, from_ = 0.0, to = 5, increment=0.5))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

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
    def __init__(self, master, name,widgetId,sort):
        self.master = master
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()
        self.value = { self.name : tk.StringVar(value = "+++")}

        self.master.entries["petName"].value["petName"].trace("u",lambda : self.updateValue(self))

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))

        self.widgets.append(tk.Entry(self.mainWidgetFrame, textvariable = self.value[self.name]))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort, sticky = "we",padx = 5, pady = 5)

    def updateValue(event,self):
        print(event,self)
        self.value[self.name].set(event)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = self.value[self.name                                                                                            ].get()
        if input == "+++" or input == "":
            return None
        return input

class checkUpSpinBoxEnt(tk.Tk):
    def __init__(self, master, name, widetId,sort):
        self.master = master
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))

        self.widgets.append(tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=1))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row =self.sort,sticky = "we",padx = 5, pady = 5)

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
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.name = name
        self.sort = sort
        self.state = False
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.value = { self.name: tk.StringVar(value = "+++")}
        self.widget = list()

        self.widget.append(tk.Button(self.mainWidgetFrame, text = self.name, command = self.buttonAction))

        self.widget[0].grid(column = 0, row = 0)

        self.mainWidgetFrame.grid(column = 0, row = self.sort ,sticky = "we",padx = 5, pady = 5)

    def buttonAction(self):
        self.state = not self.state

        if self.state == True:
            self.buttonValue.set("Αντιστροφή Ε & Α κύματος διαμιτροειδικής ροής, εύρημα συμβατό με  1ου βαθμού διαστολική δυσλειτουργία του μυοκαρδίου.")
            self.widget[0].configure(bg = "red")
        else:
            self.buttonValue.set("+++")
            self.widget[0].configure(bg = "white")

    def getWidgetValues(self):
        input = self.value[self.name].get()
        if input == "+++":
            return None
        return input

class ecgMenuEnt(tk.Tk):
    def __init__(self, master, name,widgetId,sort):
        self.master = master
        self.field = db.getWidgetMenus(self.master.master.path,widgetId)
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.frames = list()
        self.values = {self.field[0][2] : db.getValues(self.master.master.path,self.field[0][0])}
        self.value = {self.field[0][2] : list()}
        self.widgets = list()

        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def createWidgets(self):
        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)
        tempListWidgets = list()

        tempListWidgets.append(tk.Button(widgetFrame, text = "+", command = self.createWidgets))
        tempListWidgets.append(tk.Button(widgetFrame, text = "-", command = lambda x = widgetFrame: self.destroyButtonAction(x)))

        tempListWidgets.append(tk.Menubutton(widgetFrame, text = self.name))
        tempListWidgets[-1].menu = tk.Menu(tempListWidgets[-1])
        tempListWidgets[-1]["menu"] = tempListWidgets[-1].menu

        self.value[self.field[0][2]].append(tk.StringVar(value = "+++"))
        tempListWidgets[-1].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[self.field[0][2]][-1])
        for val in self.values[self.field[0][2]]:
            tempListWidgets[-1].menu.add_radiobutton(label = val[0], value = val[0],variable = self.value[self.field[2]][-1])

        tempListWidgets.append(tk.Entry(widgetFrame, text = self.value[self.field[0][2]][-1]))

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
            del self.value[self.field[0][2]][counter]
            del self.widgets[counter]

    def getWidgetValues(self):
        values = list()
        for ent in self.value[self.field[0][2]]:
            val = ent.get()
            if val == "+++" or val == "":
                pass
            else:
                values.append(val)
                self.checkSelf(val)

        if len(values) == 0:
            return None
        else:
            return values

    def checkSelf(self):
        for val in self.value[self.field[0][2]]:
            if self.values[self.field[0][2]].count(val) == 0:
                db.createValue(self.master.master.val,self.field[0][field][0])


class ageSpinBoxEnt(tk.Tk):
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.name = name
        self.sort = sort
        self.pet = self.master.master.fileSelected[2]
        self.value = {"age" : tk.StringVar(), "ageAprox" : tk.IntVar()}
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))
        self.widgets.append(tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment= 1,textvariable = self.value["age"]))

        self.widgets.append(tk.Radiobutton(self.mainWidgetFrame, variable = self.value["ageAprox"], text="Μηνών", value=1))

        self.widgets.append(tk.Radiobutton(self.mainWidgetFrame ,variable = self.value["ageAprox"], text="Ετών", value=2))
        self.widgets[-1].select()

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row =self.sort,sticky = "we",padx = 5, pady = 5)


    def giveValues(self):
        num = int(self.value["age"].get())
        approx = self.value["ageAprox"].get()

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
        age = int(self.value["age"].get())
        timeAproximation = self.value["ageAprox"].get()

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
    def __init__(self, master, name,widgetId,sort):
        self.master = master
        self.widgetMenus = db.getWidgetMenus(self.master.master.path,widgetId)
        self.sort = sort
        self.name = name
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.frames = list()
        self.value = {}
        self.values = {}
        self.fields = {}
        for menu in self.widgetMenus:
            self.value [menu[2]] = list()
            self.values [menu[2]] = db.getValues(self.master.master.path,menu[0])
            self.fields [menu[2]] = menu[0]
        self.value["doseNumber"] = list()
        self.widgets = list()

        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def createWidgets(self):
        tempListWidgets = list()

        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)

        tempListWidgets.append(tk.Button(widgetFrame, text = "+", command = self.createWidgets))
        tempListWidgets.append(tk.Button(widgetFrame, text = "-", command = lambda x = widgetFrame: self.destroyButtonAction(x)))

        for menuId in self.values:
            tempListWidgets.append(tk.Menubutton(widgetFrame, text = menuId))

            self.value[menuId].append(tk.StringVar(value = "+++"))
            tempListWidgets[-1].menu = tk.Menu(tempListWidgets[-1])
            tempListWidgets[-1]["menu"] = tempListWidgets[-1].menu
            tempListWidgets[-1].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[menuId][-1])
            for val in self.values[menuId]:
                tempListWidgets[-1].menu.add_radiobutton(label = val[0], value = val[0],variable = self.value[menuId][-1])

            tempListWidgets.append(tk.Entry(widgetFrame, textvariable = self.value[menuId][-1]))

            if menuId == "medication" or menuId == "medication2":
                self.value["doseNumber"].append(tk.StringVar(value = "0.0"))
                tempListWidgets.append(tk.Spinbox(widgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f",textvariable = self.value["doseNumber"][-1]))

        self.widgets.append(tempListWidgets)

        self.gridWidgets()
        widgetFrame.grid(column = 0, row = len(self.widgets)-1)

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

            for menu in self.values:
                del self.value[menu][counter]

            del self.widgets[counter]

    def getWidgetValues(self):
        values = list()
        flag = True

        for i in range(self.value["doseNumber"]):
            temp = {}
            for menu in self.value:
                temp[menu] = self.value[menu][i].get()

            for t in temp:
                if temp[t] == "+++" or temp[t] == "0.0":
                    flag = False

            if flag == False:
                pass
            else:
                temp["doseNumber"] = buildNumber(float(temp["doseNumber"]),self.master)
                values.append(temp)
                self.checkSelf(temp)

        if len(values) != 0:
            return values
        else:
            return None

    def checkSelf(self, value):
        for field in self.fields:
            if self.values[field].count(self.value[field]) == 0:
                db.createValue(self.master.master.path,self.value[field],self.field[field])

class pdfReader(tk.Tk):
    def __init__(self, master, name,widgetId,sort):
        self.master = master
        self.name = name
        self.sort = sort
        self.value =  tk.StringVar(value = "+++")
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Button(self.mainWidgetFrame, text = self.name, command = self.buttonAction))

        self.widgets.append(tk.Entry(self.mainWidgetFrame, text = self.value, state = 'disabled' ))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def buttonAction(self):
        fileName = filedialog.askopenfilename(filetypes = (("pdf files","*.pdf"),))
        self.value.set(fileName)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        fileName = self.value.get()
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
    def __init__(self, master, name,widgetId,sort):
        self.master = master
        self.field = db.getWidgetMenus(self.master.master.path,widgetId)
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()
        self.value =  { self.name : tk.StringVar(value = "+++") }
        self.values = { self.name : db.getValues(self.master.master.path,self.field[0][0])}

        self.widgets.append(tk.Menubutton(self.mainWidgetFrame, text = self.name))

        self.widgets[0].menu = tk.Menu(self.widgets[0])
        self.widgets[0]["menu"] = self.widgets[0].menu
        self.widgets[0].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[self.name])
        for val in self.values[self.name]:
            self.widgets[0].menu.add_radiobutton(label = val[0], value = val[0],variable = self.value[self.name])

        self.widgets.append( tk.Entry(self.mainWidgetFrame, text = self.value[name]))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort ,sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        if self.values[self.name].count(self.value[self.name].get()) == 0 :
            db.createValue(self.master.path,self.value[self.name].get(),self.self.field[0][0])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        if self.value[self.name].get() == "+++" or self.value[self.name].get() == "" :
            return None
        else:
            self.checkSelf()
            return self.value[self.name].get()

class entryEnt(tk.Tk):
    def __init__(self, master, name, nameId, widgetId,sort):
        self.master = master
        self.name = name
        self.nameId = nameId
        self.sort = sort
        self.value = { self.nameId : tk.StringVar(value = "+++")}
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.nameId))
        self.widgets.append(tk.Entry(self.mainWidgetFrame, textvariable = self.value[self.nameId]))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0,padx = 5, pady = 5)
            column += 1

    def getWidgetValues(self):
        input = self.value[self.nameId].get()
        if len(input.split()) == 0 or input == "+++":
            return None
        return input
