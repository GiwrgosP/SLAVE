import tkinter as tk
import db as db

class dogPERECardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent,inputFrame):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(inputFrame)
        self.widgets = list()
        self.value = [db.getFieldValues(183,self.master.master.path),\
        db.getFieldValues(184,self.master.master.path),\
        db.getFieldValues(185,self.master.master.path),\
        db.getFieldValues(186,self.master.master.path)]
        self.values = {"weight" : tk.StringVar(value = "+++"),\
        "age" : tk.StringVar(value = "+++"),\
        "time" : tk.StringVar(value = "+++"),\
        "dcm" : tk.StringVar(value = "+++"),\
        "cardFail" : tk.StringVar(value = "+++"),\
        "effusion" : tk.StringVar(value = "+++")}

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(widgetLabel)

        menuTime =  tk.Menubutton(self.mainWidgetFrame, text = "Αρ.επισκεψης")
        self.widgets.append(menuTime)
        self.applyValues(0)

        entryTime = tk.Entry(self.mainWidgetFrame, variable = self.values["time"])
        self.widgets.append(entryTime)

        menuDcm =  tk.Menubutton(self.mainWidgetFrame, text = "dcm")
        self.widgets.append(menuDcm)
        self.applyValues(1)

        entryDmc = tk.Entry(self.mainWidgetFrame, variable = self.values["dmc"])
        self.widgets.append(entryDmc)

        menuCardFail =  tk.Menubutton(self.mainWidgetFrame, text = "cardFail")
        self.widgets.append(menuCardFail)
        self.applyValues(2)

        entryCardFail = tk.Entry(self.mainWidgetFrame, variable = self.values["cardFail"])
        self.widgets.append(entryCardFail)

        menuEffusion =  tk.Menubutton(self.mainWidgetFrame, text = "effusion")
        self.widgets.append(menuEffusion)
        self.applyValues(3)

        entryEffusion = tk.Entry(self.mainWidgetFrame, variable = self.values["effusion"])
        self.widgets.append(entryEffusion)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def checkSelf(self):
        pass


    def refreshVar(self):
        self.values["weight"].set(self.master.entries["weight"].giveValues())
        self.values["age"].set(self.master.entries["age"].giveValues())

    def applyValues(self,pos):
        self.widgets[pos].menu = tk.Menu(self.widgets[pos])
        self.widgets[pos]["menu"] = self.widgets[pos].menu
        for val in self.value[pos]:
            if pos == 0:
                self.widgets[pos].menu.add_radiobutton(label = val, value = val,variable = self.values["time"])
            elif pos == 2:
                self.widgets[pos].menu.add_radiobutton(label = val, value = val,variable = self.values["dcm"])
            elif pos == 3:
                self.widgets[pos].menu.add_radiobutton(label = val, value = val,variable = self.values["cardFail"])
            else:
                self.widgets[pos].menu.add_radiobutton(label = val, value = val,variable = self.values["effusion"])

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
        " σκύλο "+self.values["dmc"].get() + \
        self.values["cardFail"].get() + " " + self.values["effusion"].get() + "."


def main():
    window = tk.Tk()
    window.title("Sophi's Loyal Assistant Veterinarian Edition")
    window.geometry("1024x512")
    inputFrame = tk.Frame(window)
    widget = dogPERECardiologicalAnalysisListBoxEnt(window,("a","a","a"),inputFrame)

main()
