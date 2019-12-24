import tkinter as tk
import db as db
from tkinter import messagebox
from docxtpl import DocxTemplate

class mainWindow(tk.Tk):
    def __init__(self,master):
        self.master = master
        print("Creating window")
        self.entryEntities = db.getEntryFields(self.master.path)
        self.entries = {}

        self.createInputFrame()

        self.createButtonFrame()

    def createInputFrame(self):
        self.canvas = tk.Canvas(self.master.window)

        self.inputFrame = tk.Frame(self.canvas)

        for ent in self.entryEntities:
            if ent[3] == "listbox":
                self.entries[ent[2]] = menuEnt(self,ent)
            elif ent[3] == "spinbox":
                self.entries[ent[2]] = spinBoxEnt(self,ent)
            elif ent[3] == "entry":
                self.entries[ent[2]] = entryEnt(self,ent)

        self.gridInputWidgets()
        self.canvas.update_idletasks()
        self.canvas.create_window(0, 0, anchor='nw', window=self.inputFrame)

        print("widgets")

        self.scrollBar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),yscrollcommand=self.scrollBar.set)
        self.canvas.pack(fill='both', expand=True, side='left')
        self.scrollBar.pack(fill='y', side='right')
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def createButtonFrame(self):
        self.buttonFrame = tk.Frame(self.master.window)

        self.enterData =  tk.Button(self.buttonFrame, text = "Enter Data", command = self.enterdata)
        self.enterData.pack()

        self.clearButton =  tk.Button(self.buttonFrame, text = "Clear Form", command = self.clearForm)
        self.clearButton.pack()

        self.quitButton =  tk.Button(self.buttonFrame, text="Back to form selection", command = self.quit)
        self.quitButton.pack()

        self.buttonFrame.pack(side = tk.RIGHT)

    def gridInputWidgets(self):
        row = 0
        for ent in self.entries:
            column = 0
            for widget in self.entries[ent].widgets:

                self.entries[ent].widgets[widget].grid(column = column, row = row)

                column+=1
            row += 1

    def on_mousewheel(self, event):
        scrollDir = int(event.delta/120)
        self.canvas.yview('scroll',-1*scrollDir, "units")

    def clearForm(self):
        answer = messagebox.askyesno('You do not appreciate the work that your slave has done so far','Do you need slave to clear the board and start all over?')
        if answer:
            self.clearWidgets()
        else:
            pass

    def quit(self):
        answer = messagebox.askyesno('You need to your slave to hand an other task','Do you need slave to get you bask to the form selection window?')
        if answer:
            self.goBack()
        else:
            pass

    def clearWidgets(self):
        self.canvas.destroy()
        self.createInputFrame()

    def goBack(self):
        self.master.fileSelected = None
        self.master.window.destroy()

        self.master.createWindow()

    def enterdata(self):
        str = self.master.path+"\\"+"DMVD-1-report.docx"

        doc = DocxTemplate(str)

        context = {}

        for ent in self.entryEntities:

            input = self.entries[ent[2]].widgets["input"].get()
            print(input)

            if input == "" or input == "0.0":
                pass
            else:
                if ent[3] == "spinbox":
                    temp = float(input) % 1
                    if temp == 0 and float(input) >= 1:
                        input = int(float(input))
                input = str(input)
                self.entries[ent[2]].checkSelf()
                context[ent[2]] = input


        print("CONTEXT",context)
        doc.render(context)
        str = self.master.path + "\\" + "generated_doc.docx"
        doc.save(str)
        answer = messagebox.askyesno('Make slave keep working on this form','Whip slave and make him go back to work?')
        if answer:
            self.clearWidgets()
        else:
            self.goBack()

    def giveValues(self):
        spinBoxWeight = float(self.entries["weight"].widgets["input"].get())
        spinBoxAge = float(self.entries["age"].widgets["input"].get())

        if spinBoxWeight != 0.00 and spinBoxAge != 0.00:

            if spinBoxWeight<= 15.00:
                weight = "μικρόσωμο"
            elif spinBoxWeight <= 55.00:
                weight = "μεγαλόσωμο"
            else:
                weight = "γιαγαντόσωμο"

            if spinBoxAge<= 4.00:
                age = "νεαρό"
            elif spinBoxAge <= 6.00:
                age = "ενήλικο"
            else:
                age = "υπερήλικο"

            self.entries["cardiologicalAnalysis"].values = (("Καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο με υποψία καρδιακής νόσου.",),\
                                                ("Προεγχειρητικός καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",),\
                                                ("Προληπτικός καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",),\
                                                ("Προεγχειρητικός και προληπτικός  καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",))
            self.entries["cardiologicalAnalysis"].applyValues()
        else:
            pass

class menuEnt():
    def __init__(self, master, ent):
        print("Creating mainFrame.menu")
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.widgets = {}
        self.values = db.getFieldValues(ent[0],self.master.master.path)

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

class spinBoxEnt():
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

            self.widgets["input"].configure(command = lambda: master.giveValues())

    def checkSelf(self):
        pass

class entryEnt():
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
