import tkinter as tk
import tkinter.ttk as ttk
import db as db
from tkinter import messagebox
from docxtpl import DocxTemplate
from tkinter import filedialog
import formEntries


class formWindow(tk.Tk):
    objectList = {"menuEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "spinbox": lambda self,ent:formEntries.spinBox(self,ent),\
    "entry": lambda self,ent:formEntries.entry(self,ent),\
    "mediMenu": lambda self,ent:formEntries.medicMenuEnt(self,ent),\
    "ageSpinBoxEnt": lambda self,ent:formEntries.ageSpinBoxEnt(self,ent),\
    "ecgMenuEnt": lambda self,ent:formEntries.ecgMenuEnt(self,ent),\
    "flowButtonEnt": lambda self,ent:formEntries.flowButtonEnt(self,ent),\
    "checkUpSpinBoxEn": lambda self,ent:formEntries.checkUpSpinBoxEn(self,ent),\
    "nameAitEntryEnt": lambda self,ent:formEntries.nameAitEntryEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "dogDMVD1CardiologicalAnalysisListBoxEnt": lambda self,ent:formEntries.dogDMVD1CardiologicalAnalysisListBoxEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\
    "bodyWeightSpinBoxEnt": lambda self,ent:formEntries.menuEnt(self,ent),\

    "menuEnt": lambda self,ent:formEntries.menuEnt(self,ent)}

    def __init__(self,master):
        self.master = master
        self.fileId = ent[0]
        self.fileName = ent[1]
        self.fileLocation = ent[2]
        self.entries = {}

        self.createInputFrame()

    def __del__(self):
        pass

    def createInputFrame(self):
        self.canvas = tk.Canvas(self.master.window)
        self.inputFrame = tk.Frame(self.canvas, background = "bisque" )
        self.form = db.getForm(self.master.path,self.fileId)
        #self.entryEntities = sorted(self.entryEntities,key = lambda x: x[5])
        sort = 0
        for widget in self.form:
            widgetId = widget[1]
            obj,nameId = getWidget(self.master.path,widgetId)
            name = getWidgetName(self.master.path,nameId)

            if obj == "menuEnt":
                self.entries[nameId] = formEntries.menuEnt(self,name,widetId,sort)
            elif obj == "entry":
                self.entries[nameId] = formEntries.entryEnt(self,name,widetId,sort)
            elif obj == "mediMenu":
                self.entries[nameId] = formEntries.medicMenuEnt(self,name,widetId,sort)
            elif obj == "ageSpinBoxEnt":
                self.entries[nameId] = formEntries.ageSpinBoxEnt(self,name,widetId,sort)
            elif obj == "ecgMenuEnt":
                self.entries[nameId] = formEntries.ecgMenuEnt(self,name,widetId,sort)
            elif obj == "flowButtonEnt":
                self.entries[nameId] = formEntries.flowButtonEnt(self,name,widetId,sort)
            elif obj == "checkUpSpinBoxEnt":
                self.entries[nameId] = formEntries.checkUpSpinBoxEnt(self,name,widetId,sort)
            elif obj == "nameAitEntryEnt":
                self.entries[nameId] = formEntries.nameAitEntryEnt(self,name,widetId,sort)
            elif obj == "bodyWeightSpinBoxEnt":
                self.entries[nameId] = formEntries.bodyWeightSpinBoxEnt(self,name,widetId,sort)
            elif obj == "dogDMVD1CardiologicalAnalysisListBoxEnt":
                self.entries[nameId] = formEntries.dogDMVD1CardiologicalAnalysisListBoxEnt(self,name,widetId,sort)
            elif obj == "weightSpinBoxEnt":
                self.entries[nameId] = formEntries.weightSpinBoxEnt(self,name,widetId,sort)
            elif obj == "pdfReader":
                self.entries[nameId] = formEntries.pdfReader(self,name,widetId,sort)
            elif obj == "auditoryFindingsMenuEnt":
                self.entries[nameId] = formEntries.auditoryFindingsMenuEnt(self,name,widetId,sort)
            elif obj == "dogDMVD1RECardiologicalAnalysisListBoxEnt":
                self.entries[nameId] = formEntries.dogDMVD1RECardiologicalAnalysisListBoxEnt(self,name,widetId,sort)
            elif obj == "dogDCMRECardiologicalAnalysisListBoxEnt":
                self.entries[nameId] = formEntries.dogDCMRECardiologicalAnalysisListBoxEnt(self,name,widetId,sort)
            elif obj == "dogPERECardiologicalAnalysisListBoxEnt":
                self.entries[nameId] = formEntries.dogPERECardiologicalAnalysisListBoxEnt(self,name,widetId,sort)
            elif obj == "catHCMRECardiologicalAnalysisListBoxEnt":
                self.entries[nameId] = formEntries.catHCMRECardiologicalAnalysisListBoxEnt(self,name,widetId,sort)
            elif obj == "catHOCMREardiologicalAnalysisListBoxEnt":
                self.entries[nameId] = formEntries.catHOCMREardiologicalAnalysisListBoxEnt(self,name,widetId,sort)
            elif obj == "dogPHRECardiologicalAnalysisListBoxEnt":
                self.entries[nameId] = formEntries.dogPHRECardiologicalAnalysisListBoxEnt(self,name,widetId,sort)
            elif obj == "dogPSRECardiologicalAnalysisListBoxEnt":
                self.entries[nameId] = formEntries.dogPSRECardiologicalAnalysisListBoxEnt(self,name,widetId,sort)
            elif obj == "dogSASRECardiologicalAnalysisListBoxEnt":
                self.entries[nameId] = formEntries.dogSASRECardiologicalAnalysisListBoxEnt(self,name,widetId,sort)
            elif obj == "historyMenuEnt":
                self.entries[nameId] = formEntries.historyMenuEnt(self,name,widetId,sort)
            elif obj == "breedMenuEnt":
                self.entries[nameId] = formEntries.breedMenuEnt(self,name,widetId,sort)
            else:
                print("Error with widget ",obj)
            sort += 1
        self.inputFrame.pack()
        self.createScrollbar()
        self.createButtonFrame()

    def createButtonFrame(self):
        self.buttonFrame = tk.Frame(self.master.window)

        fileSelectedLabel = tk.Label(self.buttonFrame, text = self.fileName )
        fileSelectedLabel.pack(anchor = "n")

        enterData =  tk.Button(self.buttonFrame, text = "Enter Data", command = self.enterdata)
        enterData.pack(anchor = "center")

        clearButton =  tk.Button(self.buttonFrame, text = "Clear Form", command = self.clearForm)
        clearButton.pack(anchor = "center")

        quitButton =  tk.Button(self.buttonFrame, text="Back to form selection", command = self.quit)
        quitButton.pack(anchor = "s")

        self.buttonFrame.pack(anchor = "s", fill = "both", expand = True)

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
        del self

    def enterdata(self):
        filePath = self.master.path+"\\Protipa\\" + self.fileLocation
        doc = DocxTemplate(filePath)
        context = {}

        self.loadingBar = ttk.Progressbar(self.buttonFrame, orient = "horizontal", length = 100, mode = 'determinate')
        self.loadingBar.pack(anchor = "s")

        loadingBarValue = 100/len(self.entries)
        for ent in self.entries:
            input = self.entries[ent].getWidgetValues()
            self.loadingBarProgress(loadingBarValue)

            if input == "" or input == "0.0" or input == [['', ' (0  )']] or input == None : # or ' (0.0 mg/kg po )'
                pass
            else:

                context[ent] = input

        print(context)
        doc.render(context)
        filePath = ""
        filePath = filedialog.asksaveasfilename(title = "Select file",filetypes = [("docx files","*.docx")])
        print(filePath)
        if filePath == "":
            self.loadingBar.destroy()
        else:
            filePath += ".docx"
            doc.save(filePath)
            answer = messagebox.askyesno('Make slave keep working on this form','Whip slave and make him go back to work?')
            if answer:
                self.clearWidgets()
            else:
                self.goBack()

    def loadingBarProgress(self,val):
        self.loadingBar['value'] = self.loadingBar['value'] + val
        self.buttonFrame.update_idletasks()
