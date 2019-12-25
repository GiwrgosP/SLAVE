import tkinter as tk
import db as db
from tkinter import messagebox
from docxtpl import DocxTemplate

import formEntries

class formWindow(tk.Tk):
    def __init__(self,master):

        self.master = master
        self.entryEntities = db.getEntryFields(self.master.path,self.master.fileSelected[0])

        self.entries = {}

        self.canvas = tk.Canvas(self.master.window)

        self.inputFrame = tk.Frame(self.canvas)

        self.createInputFrame()
        self.entryEntities = db.getEntryFields(self.master.path,"all")
        self.createInputFrame()
        self.gridInputWidgets()
        self.createScrollbar()
        self.createButtonFrame()

    def createInputFrame(self):


        for ent in self.entryEntities:
            if ent[3] == "listbox":
                self.entries[ent[2]] = formEntries.menuEnt(self,ent)
            elif ent[3] == "spinbox":
                self.entries[ent[2]] = formEntries.spinBoxEnt(self,ent)
            elif ent[3] == "entry":
                self.entries[ent[2]] = formEntries.entryEnt(self,ent)




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

    def gridInputWidgets(self):
        row = 0
        for ent in self.entries:
            column = 0
            for widget in self.entries[ent].widgets:

                self.entries[ent].widgets[widget].grid(column = column, row = row)

                column+=1
            row += 1

    def createScrollbar(self):
        self.canvas.update_idletasks()
        self.canvas.create_window(0, 0, anchor='nw', window=self.inputFrame)

        self.scrollBar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),yscrollcommand=self.scrollBar.set)
        self.canvas.pack(fill='both', expand=True, side='left')
        self.scrollBar.pack(fill='y', side='right')
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onMouseWheel(self, event):
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
        filePath = self.master.path+"\\"+"DMVD-1-report.docx"
        doc = DocxTemplate(filePath)
        context = {}

        for ent in self.entryEntities:

            input = self.entries[ent[2]].widgets["input"].get()

            if input == "" or input == "0.0":
                pass
            else:
                if ent[3] == "spinbox":
                    temp = float(input) % 1
                    if temp == 0 and float(input) >= 1:
                        input = int(float(input))
                temp = str(input)
                self.entries[ent[2]].checkSelf()
                context[ent[2]] = temp

        doc.render(context)
        filePath = self.master.path + "\\" + "generated_doc.docx"
        doc.save(filePath)
        answer = messagebox.askyesno('Make slave keep working on this form','Whip slave and make him go back to work?')
        if answer:
            self.clearWidgets()
        else:
            self.goBack()
