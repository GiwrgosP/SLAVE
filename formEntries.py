import tkinter as tk
import db as db

class menuEnt(tk.Tk):
    def __init__(self, master, ent):
        print("Creating mainFrame.menu")
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.widgets = {}
        self.values = db.getFieldValues(self.field,self.master.master.path)

        self.currentValue =  tk.StringVar()
        self.widgets["menuButton"] =  tk.Menubutton(self.master.inputFrame, text = self.text)

        self.applyValues()

        self.widgets["input"] = tk.Entry(self.master.inputFrame, text = self.currentValue)

    def applyValues(self):

        self.widgets["menuButton"].menu =   tk.Menu(self.widgets["menuButton"])
        self.widgets["menuButton"]["menu"] = self.widgets["menuButton"].menu

        for val in self.values:
            self.widgets["menuButton"].menu.add_radiobutton(label = val[0], variable = self.currentValue, value = val[0])

    def checkSelf(self):
        if self.currentValue in self.values:
            pass
        else:
            db.createFieldValue(self.currentValue.get(),self.field)

class spinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        print("Creating mainFrame.spinbox")
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.value = tk.DoubleVar()
        self.widgets = {}

        self.widgets["label"] = tk.Label(self.master.inputFrame, text = self.text)
        self.widgets["input"] = tk.Spinbox(self.master.inputFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f")

        if self.name == "weight" or self.name == "age":

            self.widgets["input"].configure(command = lambda: self.master.giveValues())

    def checkSelf(self):
        pass

class entryEnt(tk.Tk):
    def __init__(self, master, ent):
        print("Creating mainFrame.entry")
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.widgets = {}

        self.widgets["label"] = tk.Label(self.master.inputFrame, text = self.text)
        self.widgets["input"] = tk.Entry(self.master.inputFrame)

    def checkSelf(self):
        pass
