import tkinter as tk
import db as db
from tkinter import messagebox
from docxtpl import DocxTemplate

import formEntries


class formWindow(tk.Tk):

    def __init__(self,master):
        self.master = master
        self.entryEntities = db.getEntryFields(self.master.path,self.master.fileSelected[0]) + db.getEntryFields(self.master.path,"all")
        self.entryEntities = sorted(self.entryEntities,key = lambda x: x[0])

        self.entries = {}

        self.createInputFrame()
        self.createScrollbar()
        self.createButtonFrame()

    def createInputFrame(self):

        self.canvas = tk.Canvas(self.master.window)

        self.inputFrame = tk.Frame(self.canvas)

        for ent in self.entryEntities:
            if ent[3] == "listbox":
                self.entries[ent[2]] = formEntries.menuEnt(self,ent)
            elif ent[3] == "spinbox":
                self.entries[ent[2]] = formEntries.spinBoxEnt(self,ent)
            elif ent[3] == "entry":
                self.entries[ent[2]] = formEntries.entryEnt(self,ent)
            elif ent[3] == "mediMenu":
                self.entries[ent[2]] = formEntries.medicMenuEnt(self,ent)
            elif ent[3] == "ageSpinBoxEnt":
                self.entries[ent[2]] = formEntries.ageSpinBoxEnt(self,ent)
            elif ent[3] == "ecgMenuEnt":
                self.entries[ent[2]] = formEntries.ecgMenuEnt(self,ent)
            elif ent[3] == "flowButtonEnt":
                self.entries[ent[2]] = formEntries.flowButtonEnt(self,ent)
            elif ent[3] == "checkUpSpinBoxEnt":
                self.entries[ent[2]] = formEntries.checkUpSpinBoxEnt(self,ent)
            else:
                print("Error with widget")
            

    def createButtonFrame(self):
        self.buttonFrame = tk.Frame(self.master.window)

        self.fileSelectedLabel = tk.Label(self.buttonFrame, text = self.master.fileSelected[1])
        self.fileSelectedLabel.pack(side = tk.TOP)

        self.enterData =  tk.Button(self.buttonFrame, text = "Enter Data", command = self.enterdata)
        self.enterData.pack(side = tk.BOTTOM)

        self.clearButton =  tk.Button(self.buttonFrame, text = "Clear Form", command = self.clearForm)
        self.clearButton.pack(side = tk.BOTTOM)

        self.quitButton =  tk.Button(self.buttonFrame, text="Back to form selection", command = self.quit)
        self.quitButton.pack(side = tk.BOTTOM)

        self.buttonFrame.pack(side = tk.RIGHT)

    def createScrollbar(self):
        self.canvas.update_idletasks()
        self.canvas.create_window(0, 0, anchor='nw', window=self.inputFrame)

        self.scrollBar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.scrollBar.pack(fill='y', side='right')

        self.canvas.configure(scrollregion=self.canvas.bbox('all'),yscrollcommand=self.scrollBar.set)

        self.updateScrollBar()

        self.canvas.pack(fill='both', expand=True, side='left')

        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def updateScrollBar(self):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),yscrollcommand=self.scrollBar.set)

    def onMouseWheel(self, event):
        scrollDir = int(event.delta/120)
        self.canvas.yview('scroll',-1*scrollDir, "units")
        self.updateScrollBar()

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
        self.buttonFrame.destroy()
        self.createInputFrame()

    def goBack(self):
        self.master.fileSelected = None
        self.master.window.destroy()
        self.master.createWindow()

    def enterdata(self):
        filePath = self.master.path+"\\Protipa\\" + "DMVD-1-report.docx"
        doc = DocxTemplate(filePath)
        context = {}

        for ent in self.entries:
            input = self.entries[ent].getWidgetValues()

            if input == "" or input == "0.0" or input == [['', ' (0.0  )']] or input == None : # or ' (0.0 mg/kg po )'
                pass
            else:
                context[ent] = input

        print(context)
        doc.render(context)

        filePath = self.master.path + "\\Protipa\\" + "generated_doc.docx"
        doc.save(filePath)
        answer = messagebox.askyesno('Make slave keep working on this form','Whip slave and make him go back to work?')
        if answer:
            self.clearWidgets()
        else:
            self.goBack()
