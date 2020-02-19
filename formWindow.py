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
        self.entries = {

        }
        self.createInputFrame()

    def __del__(self):
        pass

    def createInputFrame(self):
        self.entryEntities = db.getEntryFields(self.master.path,self.master.fileSelected[0]) + db.getEntryFields(self.master.path,"all")
        self.entryEntities = sorted(self.entryEntities,key = lambda x: x[5])
        self.canvas = tk.Canvas(self.master.window)

        self.inputFrame = tk.Frame(self.canvas, background = "bisque" )


        for ent in self.entryEntities:
            if ent[4] == "menuEnt":
                self.entries[ent[2]] = formEntries.menuEnt(self,ent)
            elif ent[4] == "spinbox":
                self.entries[ent[2]] = formEntries.spinBoxEnt(self,ent)
            elif ent[4] == "entry":
                self.entries[ent[2]] = formEntries.entryEnt(self,ent)
            elif ent[4] == "mediMenu":
                self.entries[ent[2]] = formEntries.medicMenuEnt(self,ent)
            elif ent[4] == "ageSpinBoxEnt":
                self.entries[ent[2]] = formEntries.ageSpinBoxEnt(self,ent)
            elif ent[4] == "ecgMenuEnt":
                self.entries[ent[2]] = formEntries.ecgMenuEnt(self,ent)
            elif ent[4] == "flowButtonEnt":
                self.entries[ent[2]] = formEntries.flowButtonEnt(self,ent)
            elif ent[4] == "checkUpSpinBoxEnt":
                self.entries[ent[2]] = formEntries.checkUpSpinBoxEnt(self,ent)
            elif ent[4] == "nameAitEntryEnt":
                self.entries[ent[2]] = formEntries.nameAitEntryEnt(self,ent)
            elif ent[4] == "bodyWeightSpinBoxEnt":
                self.entries[ent[2]] = formEntries.bodyWeightSpinBoxEnt(self,ent)
            elif ent[4] == "dogDMVD1CardiologicalAnalysisListBoxEnt":
                self.entries[ent[2]] = formEntries.dogDMVD1CardiologicalAnalysisListBoxEnt(self,ent)
            elif ent[4] == "weightSpinBoxEnt":
                self.entries[ent[2]] = formEntries.weightSpinBoxEnt(self,ent)
            elif ent[4] == "pdfReader":
                self.entries[ent[2]] = formEntries.pdfReader(self,ent)
            elif ent[4] == "auditoryFindingsMenuEnt":
                self.entries[ent[2]] = formEntries.auditoryFindingsMenuEnt(self,ent)
            elif ent[4] == "dogDMVD1RECardiologicalAnalysisListBoxEnt":
                self.entries[ent[2]] = formEntries.dogDMVD1RECardiologicalAnalysisListBoxEnt(self,ent)
            elif ent[4] == "dogDCMRECardiologicalAnalysisListBoxEnt":
                self.entries[ent[2]] = formEntries.dogDCMRECardiologicalAnalysisListBoxEnt(self,ent)
            elif ent[4] == "dogPERECardiologicalAnalysisListBoxEnt":
                self.entries[ent[2]] = formEntries.dogPERECardiologicalAnalysisListBoxEnt(self,ent)
            elif ent[4] == "catHCMRECardiologicalAnalysisListBoxEnt":
                self.entries[ent[2]] = formEntries.catHCMRECardiologicalAnalysisListBoxEnt(self,ent)
            elif ent[4] == "catHOCMREardiologicalAnalysisListBoxEnt":
                self.entries[ent[2]] = formEntries.catHOCMREardiologicalAnalysisListBoxEnt(self,ent)
            elif ent[4] == "dogPHRECardiologicalAnalysisListBoxEnt":
                self.entries[ent[2]] = formEntries.dogPHRECardiologicalAnalysisListBoxEnt(self,ent)
            elif ent[4] == "dogPSRECardiologicalAnalysisListBoxEnt":
                self.entries[ent[2]] = formEntries.dogPSRECardiologicalAnalysisListBoxEnt(self,ent)
            elif ent[4] == "dogSASRECardiologicalAnalysisListBoxEnt":
                self.entries[ent[2]] = formEntries.dogSASRECardiologicalAnalysisListBoxEnt(self,ent)
            elif ent[4] == "historyMenuEnt":
                self.entries[ent[2]] = formEntries.historyMenuEnt(self,ent)
            elif ent[4] == "breedMenuEnt":
                self.entries[ent[2]] = formEntries.breedMenuEnt(self,ent)
            else:
                print("Error with widget")

        self.inputFrame.pack()
        self.createScrollbar()
        self.createButtonFrame()

    def createButtonFrame(self):
        self.buttonFrame = tk.Frame(self.master.window)

        fileSelectedLabel = tk.Label(self.buttonFrame, text = self.master.fileSelected[1] + " " + self.master.fileSelected[-2] + self.master.fileSelected[-1])
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
        filePath = self.master.path+"\\Protipa\\" + "DMVD-1-report.docx"
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
