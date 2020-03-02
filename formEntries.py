import tkinter as tk
from tkinter import filedialog
import tika
from tika import parser
import re
from decimal import *


def frameBgColor(ent):
    if ent == 0:
        return "sky blue"
    else:
        if ent % 2 == 0:
            return "sky blue"
        else:
            return "light cyan"

def replaceValues(values,value):
    result = list()
    for sentence in values:
        temp = sentence
        for word in value:
            temp = temp.replace(word[::-1],value[word].get())

        result.append(temp)

    return result

class breedMenuEnt(tk.Tk):
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.field = self.master.master.getWidgetMenus(widgetId)[0]
        self.name = name
        self.sort = sort
        self.pet = self.master.pet
        self.value =  { self.field[0] : tk.StringVar(value = "+++") }
        self.values = { self.field[0] : self.master.master.getValues(self.field[0]) }
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Menubutton(self.mainWidgetFrame, text = self.name))
        self.widgets[0].menu =   tk.Menu(self.widgets[0])
        self.widgets[0]["menu"] = self.widgets[0].menu
        self.widgets[0].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[self.field[0]])

        for val in self.values[self.field[0]]:
            self.widgets[0].menu.add_radiobutton(label = val, value = val,variable = self.value[self.field[0]])

        self.widgets.append(tk.Entry(self.mainWidgetFrame, text = self.value[self.field[0]]))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        if self.values[self.field[0]].count(self.value[self.field[0]].get()) == 0:
            self.master.master.createValue(self.value[self.field[0]].get(),self.field[0])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        if self.value[self.field[0]].get() == "+++" or self.value[self.field[0]].get() == "":
            return None
        else:
            self.checkSelf()
            return self.value[self.field[0]].get()

class historyMenuEnt(tk.Tk):
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.field = self.master.master.getWidgetMenus(widgetId)[0]
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.frames = list()
        self.values = {self.field[0] : self.master.master.getValues(self.field[0])}
        self.value = {self.field[0]: list()}
        self.widgets = list()

        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort, sticky = "we", padx = 5, pady = 5)

    def createWidgets(self):
        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)

        tempList = list()

        tempList.append(tk.Button(widgetFrame, text = "+", command = self.createWidgets))
        tempList.append(tk.Button(widgetFrame, text = "-", command = lambda x = widgetFrame: self.destroyButtonAction(x)))

        self.value[self.field[0]].append(tk.StringVar(value = "+++"))

        tempList.append(tk.Menubutton(widgetFrame, text = self.name))
        tempList[-1].menu = tk.Menu(tempList[-1])
        tempList[-1]["menu"] = tempList[-1].menu
        tempList[-1].menu.add_radiobutton(label = "+++", value = "+++", variable = self.value[self.field[0]][-1])

        for val in self.values[self.field[0]]:
            tempList[-1].menu.add_radiobutton(label = val, value = val,variable = self.value[self.field[0]][-1])

        tempList.append( tk.Entry(widgetFrame, width = 120 ,textvariable = self.value[self.field[0]][-1]))


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
        for ent in self.value[self.field[0]]:
            val = ent.get()
            if val == "+++" or val == "" :
                pass
            else:
                values.append(val)
        if len(values) == 0:
            return None
        else:
            return values

class dogDMVD1CardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, name, widgetId,sort):
        self.master = master
        self.widgetMenus = self.master.master.getWidgetMenus(widgetId)[0]
        self.name = name
        self.sort = sort
        self.state = False
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()
        self.value = {"weight" : tk.StringVar(value = "+++"), "age" : tk.StringVar(value = "+++"), "cardiologicalAnalysis" : tk.StringVar(value = "")}

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))

        self.widgets.append(tk.Menubutton(self.mainWidgetFrame, text = self.widgetMenus[0]))

        self.master.entries["weight"].value["weight"].trace_add("write",  self.updateValueWeight)
        self.master.entries["age"].value["age"].trace_add("write", self.updateValueAge)
        self.master.entries["age"].value["ageAprox"].trace_add("write", self.updateValueAge)

        self.updateState()

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = self.value["cardiologicalAnalysis"].get()
        if input == "+++" or input == "":
            return None
        return input

    def updateValueWeight(self, *args):
        val = float(self.master.entries["weight"].value["weight"].get())

        if val == 0.0:
            self.value["weight"].set("+++")
        else:
            self.value["weight"].set(self.master.calcWeight(val))
        self.updateState()

    def updateValueAge(self, *args):
        age = int(self.master.entries["age"].value["age"].get())
        approx = self.master.entries["age"].value["ageAprox"].get()

        if approx == 1:
            self.value["age"].set("νεαρο")
        else:
            self.value["age"].set(self.master.calcAge(age))

        self.updateState()

    def applyValues(self):
        try:
            self.widgets[1].menu.destroy()
        except:
            pass
        self.values = replaceValues(self.master.master.getValues(self.widgetMenus[0]),self.value)

        self.widgets[1].menu =   tk.Menu(self.widgets[1])
        self.widgets[1]["menu"] = self.widgets[1].menu
        self.widgets[1].menu.add_radiobutton(label = "+++", value ="+++",variable = self.value["cardiologicalAnalysis"])

        for val in self.values:
            self.widgets[1].menu.add_radiobutton(label = val, value = val,variable = self.value["cardiologicalAnalysis"])

    def updateState(self):
        if self.value["weight"].get() == "+++" or self.value["age"].get() == "+++":
            self.widgets[-1].configure(state = "disabled")
        else:
            self.widgets[-1].configure(state = "normal")
            self.applyValues()

class dogDMVD1RECardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.widgetMenus = self.master.master.getWidgetMenus(widgetId)[0]
        self.name = name
        self.sort = sort
        self.state = False
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()
        self.value = {"weight" : tk.StringVar(value = "+++"),\
        "age" : tk.StringVar(value = "+++")}
        self.values = {}

        self.master.entries["weight"].value["weight"].trace_add("write",  self.updateValueWeight)
        self.master.entries["age"].value["age"].trace_add("write", self.updateValueAge)
        self.master.entries["age"].value["ageAprox"].trace_add("write", self.updateValueAge)

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))
        for menu in self.widgetMenus:
            self.value [menu] = tk.StringVar(value = "+++")
            self.values [menu] = self.master.master.getValues(menu)

            self.widgets.append(tk.Menubutton(self.mainWidgetFrame, text = menu ))
            self.widgets[-1].menu = tk.Menu(self.widgets[-1])
            self.widgets[-1]["menu"] = self.widgets[-1].menu

            self.widgets[-1].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[menu])
            for val in self.values[menu]:
                self.widgets[-1].menu.add_radiobutton(label = val, value = val,variable = self.value[menu])
        self.updateState()
        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1,sticky = "we",padx = 5, pady = 5)

    def updateValueWeight(self, *args):
        val = float(self.master.entries["weight"].value["weight"].get())

        if val == 0.0:
            self.value["weight"].set("+++")
        else:
            self.value["weight"].set(self.master.calcWeight(val))
        self.updateState()

    def updateValueAge(self, *args):
        age = int(self.master.entries["age"].value["age"].get())
        approx = self.master.entries["age"].value["ageAprox"].get()

        if approx == 1:
            self.value["age"].set("νεαρο")
        else:
            self.value["age"].set(self.master.calcAge(age))

        self.updateState()

    def updateState(self):
        if self.value["weight"].get() == "+++" or self.value["age"].get() == "+++":
            for i in range(len(self.widget.[1:])-1) :
                self.widgets[i].configure(state = "disabled")
        else:
            for i in range(len(self.widget.[1:])-1) :
                self.widgets[i].configure(state = "normal")

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        flag = False
        for menu in self.value:
            if self.value[menu].get() != "+++"

class auditoryFindingsMenuEnt(tk.Tk):
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.widgetMenus = self.master.master.getWidgetMenus(widgetId)
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.fields = {}
        self.value = {}
        self.values = {}
        for menu in self.widgetMenus:
            self.value [menu[0]] = tk.StringVar(value = "+++")
            self.values [menu[0]] = self.master.master.getValues(menu[0])
            self.fields [menu[0]] = menu[0]

        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name ))

        for menuId in self.values:
            self.widgets.append(tk.Menubutton(self.mainWidgetFrame, text = menuId ))
            self.widgets[-1].menu = tk.Menu(self.widgets[-1])
            self.widgets[-1]["menu"] = self.widgets[-1].menu

            self.widgets[-1].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[menuId])
            for val in self.values[menuId]:
                self.widgets[-1].menu.add_radiobutton(label = val, value = val,variable = self.value[menuId])


        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort ,sticky = "we",padx = 5, pady = 5)

    def getWidgetValues(self):
        flag = True
        temp = {}
        for menu in self.value:
            if self.value[menu].get() == "+++" :
                flag = False
                break
            else:
                temp[menu] = self.value[menu].get()

        if flag == True:
            return temp
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
        self.value = { "weight" : tk.StringVar(value = "0.0")}
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))

        self.widgets.append(tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f", textvariable = self.value["weight"]))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = float(self.widgets[1].get())
        if input == 0.0:
            return None
        return self.master.buildNumber(input)

class bodyWeightSpinBoxEnt(tk.Tk):
    def __init__(self, master, name, widgetId,sort):
        self.master = master
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()
        self.field = self.master.master.getWidgetMenus(widgetId)[0]
        self.values = { self.name : self.master.master.getValues(self.field[0])}
        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))

        self.widgets.append(tk.Spinbox(self.mainWidgetFrame, from_ = 0.0, to = 5, increment=0.5))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def getWidgetValues(self):
        num = float(self.widgets[1].get())
        if num == 1.5:
            return None
        elif num <  1.5:
            input = self.values[self.name][0]
        elif num < 2.5:
            input = self.values[self.name][1]
        elif num <= 4.0:
            input = self.values[self.name][2]
        elif num <= 5:
            input = self.values[self.name][3]
        else:
            print("Error with widget ", self.name, num)
            return None

        temp = self.master.buildNumber(num)
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
        self.state = False
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()
        self.value = { self.name : tk.StringVar(value = "+++")}

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))

        self.widgets.append(tk.Entry(self.mainWidgetFrame, textvariable = self.value[self.name]))

        self.master.entries["petName"].value["petName"].trace_add("write", self.updateValue)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort, sticky = "we",padx = 5, pady = 5)

    def updateValue(self,*args):
        val = self.master.entries["petName"].value["petName"].get()
        self.value[self.name].set(val)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column+=1

    def getWidgetValues(self):
        input = self.value[self.name].get()
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
        if curDate!= None and self.widgets[1].get() != "0":
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
            self.value[self.name].set("Αντιστροφή Ε & Α κύματος διαμιτροειδικής ροής, εύρημα συμβατό με  1ου βαθμού διαστολική δυσλειτουργία του μυοκαρδίου.")
            self.widget[0].configure(bg = "red")
        else:
            self.value[self.name].set("+++")
            self.widget[0].configure(bg = "white")

    def getWidgetValues(self):
        input = self.value[self.name].get()
        if input == "+++":
            return None
        return input

class ecgMenuEnt(tk.Tk):
    def __init__(self, master, name,widgetId,sort):
        self.master = master
        self.field = self.master.master.getWidgetMenus(widgetId)[0]
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.frames = list()
        self.values = {self.field[0] : self.master.master.getValues(self.field[0])}
        self.value = {self.field[0] : list()}
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

        self.value[self.field[0]].append(tk.StringVar(value = "+++"))
        tempListWidgets[-1].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[self.field[0]][-1])
        for val in self.values[self.field[0]]:
            tempListWidgets[-1].menu.add_radiobutton(label = val, value = val,variable = self.value[self.field[0]][-1])

        tempListWidgets.append(tk.Entry(widgetFrame, text = self.value[self.field[0]][-1]))

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
            del self.value[self.field[0]][counter]
            del self.widgets[counter]

    def getWidgetValues(self):
        values = list()
        for ent in self.value[self.field[0]]:
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

    def checkSelf(self,val):
        print(val,self.field[0])
        for val in self.value[self.field[0]]:
            if self.values[self.field[0]].count(val.get()) == 0:
                self.master.master.createValue(val.get(),self.field[0])

class ageSpinBoxEnt(tk.Tk):
    def __init__(self, master, name, widgetId, sort):
        self.master = master
        self.name = name
        self.sort = sort
        self.pet = self.master.pet
        self.value = {"age" : tk.StringVar(value = "0"), "ageAprox" : tk.IntVar(value = 2)}
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))
        self.widgets.append(tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment= 1,textvariable = self.value["age"]))

        self.widgets.append(tk.Radiobutton(self.mainWidgetFrame, variable = self.value["ageAprox"], text="Μηνών",value = 1))

        self.widgets.append(tk.Radiobutton(self.mainWidgetFrame , variable = self.value["ageAprox"], text="Ετών", value = 2))
        self.widgets[-1].select()


        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row =self.sort,sticky = "we",padx = 5, pady = 5)

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
        self.widgetMenus = self.master.master.getWidgetMenus(widgetId)
        self.sort = sort
        self.name = name
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.frames = list()
        self.value = {}
        self.values = {}
        self.fields = {}
        for menu in self.widgetMenus:
            self.value [menu[0]] = list()
            self.values [menu[0]] = self.master.master.getValues(menu[0])
            self.fields [menu[0]] = menu[0]
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
        tempListWidgets.append(tk.Label(widgetFrame, text = self.name))

        for menuId in self.values:
            tempListWidgets.append(tk.Menubutton(widgetFrame, text = menuId))

            self.value[menuId].append(tk.StringVar(value = "+++"))
            tempListWidgets[-1].menu = tk.Menu(tempListWidgets[-1])
            tempListWidgets[-1]["menu"] = tempListWidgets[-1].menu
            tempListWidgets[-1].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[menuId][-1])
            for val in self.values[menuId]:
                tempListWidgets[-1].menu.add_radiobutton(label = val, value = val,variable = self.value[menuId][-1])

            tempListWidgets.append(tk.Entry(widgetFrame, textvariable = self.value[menuId][-1]))

            if menuId == "medicationGreekMenu" or menuId == "medication2GreekMenu":
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

        for i in range(len(self.value["doseNumber"])):
            temp = {}
            for menu in self.value:
                temp[menu] = self.value[menu][i].get()

            for t in temp:
                if temp[t] == "+++" or temp[t] == "0.0":
                    flag = False

            if flag == False:
                pass
            else:
                temp["doseNumber"] = self.master.buildNumber(float(temp["doseNumber"]))
                values.append(temp)
                self.checkSelf(temp)

        if len(values) != 0:
            return values
        else:
            return None

    def checkSelf(self, value):
        for field in self.fields:
            print(field)
            if self.values[field].count(value[field]) == 0:
                self.master.master.createValue(value[field],self.fields[field])

class photoReader(tk.Tk):
    def __init__(self, master, name,widgetId,sort):
        self.master = master
        self.name = name
        self.sort = sort
        self.value =  { "filePath" : tk.StringVar(value = "+++"), "files" : None }
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Button(self.mainWidgetFrame, text = self.name, command = self.buttonAction))

        self.widgets.append(tk.Entry(self.mainWidgetFrame, text = self.value["filePath"], state = 'disabled' ))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort,sticky = "we",padx = 5, pady = 5)

    def buttonAction(self):
        fileName = filedialog.askdirectory()
        import os
        if fileName != None:
            self.value["files"] = os.listdir(fileName)
            print()
            if len(self.widgets) > 2:
                for i in range(len(self.widgets)-1,2,-1):
                    self.widgets[i].destroy()
                    del self.widgets[i]

            for file in self.value["files"]:
                self.widgets.append(tk.Label(self.mainWidgetFrame, text = file))

            self.gridWidgets()

        else:
            pass


    def gridWidgets(self):
        column = 0
        row = 0
        for ent in self.widgets:
            if column == 5:
                row += 1
                column = 2
            ent.grid(column = column, row = row)
            column += 1

    def getWidgetValues(self):
        if self.value["files"] != None and len(self.value["files"]) != 0:
            return self.value["files"]
        else:
            return None

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
            tags = self.master.master.getEksetasi()
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

                input[i] = self.master.buildNumber(temp)

        return input

class menuEnt(tk.Tk):
    def __init__(self, master, name,widgetId,sort):
        self.master = master
        self.field = self.master.master.getWidgetMenus(widgetId)[0]
        self.name = name
        self.sort = sort
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()
        self.value =  { self.name : tk.StringVar(value = "+++") }
        self.values = { self.name : self.master.master.getValues(self.field[0])}

        self.widgets.append(tk.Menubutton(self.mainWidgetFrame, text = self.name))

        self.widgets[0].menu = tk.Menu(self.widgets[0])
        self.widgets[0]["menu"] = self.widgets[0].menu
        self.widgets[0].menu.add_radiobutton(label = "+++", value = "+++",variable = self.value[self.name])
        for val in self.values[self.name]:
            self.widgets[0].menu.add_radiobutton(label = val, value = val,variable = self.value[self.name])

        self.widgets.append( tk.Entry(self.mainWidgetFrame, text = self.value[self.name]))

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = self.sort ,sticky = "we",padx = 5, pady = 5)

    def checkSelf(self):
        if self.values[self.name].count(self.value[self.name].get()) == 0 :
            self.master.master.createValue(self.value[self.name].get(),self.field[0])

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
    def __init__(self, master, name, widgetId,sort):
        self.master = master
        self.name = name
        self.nameId = widgetId
        self.sort = sort
        self.value = { self.nameId : tk.StringVar(value = "+++")}
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets = list()

        self.widgets.append(tk.Label(self.mainWidgetFrame, text = self.name))
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
