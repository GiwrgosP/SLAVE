import tkinter as tk
import db as db
from tkinter import filedialog
import tika
from tika import parser
from decimal import *

#background coloring
def frameBgColor(ent):
    if ent == 0:
        return "alice blue"
    else:
        temp = ent % 2
        if temp == 0:
            return "cornsilk"
        else:
            return "light gray"

#Αντικαταστάσεις στους αριθμούς
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

#Είδος του ζώου
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
