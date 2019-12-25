import tkinter as tk
import db as db

class menuEnt(tk.Tk):
    def __init__(self, master, ent):
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
            db.createFieldValue(self.master.master.path,self.currentValue.get(),self.field)

class spinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.value = tk.DoubleVar()
        self.widgets = {}

        self.widgets["label"] = tk.Label(self.master.inputFrame, text = self.text)
        self.widgets["input"] = tk.Spinbox(self.master.inputFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f")

        if self.name == "weight" or self.name == "age":
            self.widgets["input"].configure(command = lambda: self.giveValues())

    def checkSelf(self):
        pass

    def giveValues(self):
        spinBoxWeight = float(self.master.entries["weight"].widgets["input"].get())
        spinBoxAge = float(self.master.entries["age"].widgets["input"].get())

        if spinBoxWeight != 0.00 and spinBoxAge != 0.00:

            if spinBoxWeight<= 15.00:
                weight = "μικρόσωμο"
            elif spinBoxWeight <= 55.00:
                weight = "μεγαλόσωμο"
            else:
                weight = "γιαγαντόσωμο"

            if spinBoxAge<= 4.00:
                age = "νεαρό"
            elif spinBoxAge <= 8.00:
                age = "ενήλικο"
            else:
                age = "υπερήλικο"

            self.master.entries["cardiologicalAnalysis"].values = (("Καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο με υποψία καρδιακής νόσου.",),\
                                                ("Προεγχειρητικός καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",),\
                                                ("Προληπτικός καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",),\
                                                ("Προεγχειρητικός και προληπτικός  καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",))
            self.master.entries["cardiologicalAnalysis"].applyValues()
        else:
            pass

class entryEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.widgets = {}

        self.widgets["label"] = tk.Label(self.master.inputFrame, text = self.text)
        self.widgets["input"] = tk.Entry(self.master.inputFrame)

    def checkSelf(self):
        pass
