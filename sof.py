import tkinter as tk
from tkinter import messagebox
from docx import Document
from docxtpl import DocxTemplate
import db as db
import os

class mainWindow(tk.Tk):
    def __init__(self):
        print("Creating window")
        self.entryEntities = db.getEntryFields()
        self.entries = {}

        self.window = tk.Tk()
        self.window.title("Sophi's Loyal Assistant Vet Edition")
        self.window.geometry("1024x512")

        self.createInputFrame()
        self.gridInputWidgets()
        self.createButtonFrame()

        self.window.mainloop()

    def createInputFrame(self):
        self.canvas = tk.Canvas(self.window)

        self.inputFrame = tk.Frame(self.canvas)

        for ent in self.entryEntities:
            if ent[3] == "listbox":
                self.entries[ent[2]] = menuEnt(self,ent)
            elif ent[3] == "spinbox":
                self.entries[ent[2]] = spinBoxEnt(self,ent)
            elif ent[3] == "entry":
                self.entries[ent[2]] = entryEnt(self,ent)


        self.canvas.update_idletasks()
        self.canvas.create_window(0, 0, anchor='nw', window=self.inputFrame)

        print("widgets")

        self.scrollBar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),yscrollcommand=self.scrollBar.set)
        self.canvas.pack(fill='both', expand=True, side='left')
        self.scrollBar.pack(fill='y', side='right')
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def createButtonFrame(self):
        self.buttonFrame = tk.Frame(self.window)

        self.enterData =  tk.Button(self.buttonFrame, text = "Enter Data", command = self.enterdata)
        self.enterData.pack()

        self.quitButton =  tk.Button(self.buttonFrame, text="Quit", command = self.quit)
        self.quitButton.pack()

        self.buttonFrame.pack(side = tk.RIGHT)

    def gridInputWidgets(self):
        pass

    def on_mousewheel(self, event):
        scrollDir = int(event.delta/120)
        self.canvas.yview('scroll',-1*scrollDir, "units")

    def quit(self):
        answer = messagebox.askyesno('Let your slave rest','Do you think it is time for your slave to rest?')
        if answer:
            exit()
        else:
            self.canvas.destroy()
            self.createFrame()

    def enterdata(self):
        entryEntities = self.entryEntities
        entries = self.entries

        doc = DocxTemplate('C:\Python37-64\sof\DMVD-1-report.docx') #++++++++++++++++++++++ ALLAGI URL************* MIN ALLAXEIS TO ONOMA TOU ARXEIOU
        context = {}
        for ent in entryEntities:

            input = entries[ent[2]].widgetInput.get()
            print(input)

            if input == "" or input == "0.00":
                pass
            else:
                context[ent[2]] = input
                entries[ent[2]].checkSelf()

        print("CONTEXT",context)
        doc.render(context)
        doc.save("C:\Python37-64\sof\generated_doc.docx")  #++++++++++++++++++++++ ALLAGI URL************* MIN ALLAXEIS TO ONOMA TOU ARXEIOU

        answer = messagebox.askyesno('Make slave keep working','Whip slave and make him go back to work?')
        if answer:
            self.canvas.destroy()
            self.createInputFrame()

        else:
            self.quit()

    def giveValues(self):
        print(self)
        #for ent in fieldDict:
        #    self.entries[ent].values = fieldDict[ent]
        #    self.entries[ent].widgetMenu.menu.destroy()

        #    self.entries[ent].applyValues()



class menuEnt():
    def __init__(self, master, ent):
        print("Creating mainFrame.menu")
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.values = db.getFieldValues(ent[0])

        self.currentValue =  tk.StringVar()
        self.widgetMenu =  tk.Menubutton(self.master.inputFrame, text = self.text)

        self.applyValues()

        self.widgetMenu.pack()
        self.widgetInput.pack()


    def applyValues(self):

        self.widgetMenu.menu =   tk.Menu(self.widgetMenu)
        self.widgetMenu["menu"] = self.widgetMenu.menu

        for val in self.values:
            self.widgetMenu.menu.add_radiobutton(label = val[0], variable = self.currentValue, value = val[0])

        self.widgetInput = tk.Entry(self.master.inputFrame, text = self.currentValue)


    def checkSelf(self):
        if self.currentValue in self.values:
            pass
        else:
            db.createFieldValue(self.currentValue.get(),self.field)

class spinBoxEnt():
    def __init__(self, master, ent):
        print("Creating mainFrame.spinbox")
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.currentValue =  tk.StringVar()

        self.widgetLabel =   tk.Label(self.master.inputFrame, text = self.text)
        self.widgetInput =  tk.Spinbox(self.master.inputFrame, from_ = 0, to = 1000, increment=0.01 , format= "%.2f")

        self.widgetLabel.pack()
        self.widgetInput.pack()

    def analyzeValue(self):
        valueFrom = float(self.widgetInput.get())
        widgetFrom = self.name
        widgetTo = {}
        valueTo = ""
        if widgetFrom == "weight":
            if valueFrom<= 15.00:
                valueTo = "μικρόσωμο"
            elif valueFrom <= 55.00:
                valueTo = "μεγαλόσωμο"
            else:
                valueTo = "γιαγαντόσωμο"

            widgetTo["cardiologicalAnalysis"] = (("Καρδιολογικός έλεγχος σε "+valueTo+"σκύλο με υποψία καρδιακής νόσου.",),\
                                                ("Προεγχειρητικός καρδιολογικός έλεγχος σε "+valueTo+"σκύλο.",),\
                                                ("Προληπτικός καρδιολογικός έλεγχος σε "+valueTo+" σκύλο.",),\
                                                ("Προεγχειρητικός και προληπτικός  καρδιολογικός έλεγχος σε "+valueTo+" σκύλο.",))

            self.master.giveValues(self.master,widgetTo)

        elif widgetFrom == "age":
            pass
        else:
            pass

class entryEnt():
    def __init__(self, master, ent):
        print("Creating mainFrame.entry")
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.widgetLabel =   tk.Label(self.master.inputFrame, text = self.text)
        self.widgetInput =  tk.Entry(self.master.inputFrame)

        self.widgetLabel.pack()
        self.widgetInput.pack()



def main():
    root = mainWindow()


main()
