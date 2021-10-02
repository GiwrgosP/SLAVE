import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from docxtpl import DocxTemplate, InlineImage
from tkinter import filedialog
import formEntries

class formWindow(tk.Tk):

    def __del__(self):
        self.buttonFrame.destroy()
        self.mainFrame.destoy()
        for ent in self.entries:
            del self.entries[ent]
        for ent in self.entries:
            self.entries[ent].destroy
        print("Ending formWindow")

    def __init__(self,master):
        self.master = master
        self.fileId = self.master.fileSelected[0]
        self.testName = self.master.fileSelected[1]
        self.language = self.master.fileSelected[2]
        self.pet = self.master.fileSelected[3]
        self.fileLocation = self.master.fileSelected[4]
        self.entries = {}
        self.mainFrame = tk.Frame(self.master.window)
        self.createInputFrame()
        self.mainFrame.pack(fill = "both", expand = True)

    def createInputFrame(self):
        self.canvas = tk.Canvas(self.mainFrame)

        self.inputFrame = tk.Frame(self.canvas, background = "bisque" )
        self.form = self.master.getForm(self.fileId)

        for widget in self.form:
            widgetId = widget[0]
            obj,name,nameVal,sort = self.master.getWidget(widgetId)

            if obj == "menuEnt":
                self.entries[name] = formEntries.menuEnt(self,nameVal,name,widgetId,sort)
            elif obj == "entry":
                self.entries[name] = formEntries.entryEnt(self,nameVal,widgetId,sort)
            elif obj == "mediMenu":
                self.entries[name] = formEntries.medicMenuEnt(self,nameVal,widgetId,sort)
            elif obj == "ageSpinBoxEnt":
                self.entries[name] = formEntries.ageSpinBoxEnt(self,nameVal,widgetId,sort)
            elif obj == "ecgMenuEnt":
                self.entries[name] = formEntries.ecgMenuEnt(self,nameVal,widgetId,sort)
            elif obj == "flowButtonEnt":
                self.entries[name] = formEntries.flowButtonEnt(self,nameVal,widgetId,sort)
            elif obj == "checkUpSpinBoxEnt":
                self.entries[name] = formEntries.checkUpSpinBoxEnt(self,nameVal,widgetId,sort)
            elif obj == "nameAitEntryEnt":
                self.entries[name] = formEntries.nameAitEntryEnt(self,nameVal,widgetId,sort)
            elif obj == "bodyWeightSpinBoxEnt":
                self.entries[name] = formEntries.bodyWeightSpinBoxEnt(self,nameVal,widgetId,sort)
            elif obj == "dogDMVDCardiologicalAnalysisEnt":
                self.entries[name] = formEntries.dogDMVDCardiologicalAnalysisListBoxEnt(self,nameVal,widgetId,sort)
            elif obj == "weightSpinBoxEnt":
                self.entries[name] = formEntries.weightSpinBoxEnt(self,nameVal,widgetId,sort)
            elif obj == "pdfReader":
                self.entries[name] = formEntries.pdfReader(self,nameVal,widgetId,sort)
            elif obj == "auditoryFindingsMenuEnt":
                self.entries[name] = formEntries.auditoryFindingsMenuEnt(self,nameVal,widgetId,sort)
            elif obj == "RECardiologicalAnalysisListBoxEnt":
                self.entries[name] = formEntries.dogDMVDRECardiologicalAnalysisListBoxEnt(self,nameVal,widgetId,sort)
            elif obj == "photoReader":
                self.entries[name] = formEntries.photoReader(self,nameVal,widgetId,sort)
            elif obj == "historyMenuEnt":
                self.entries[name] = formEntries.historyMenuEnt(self,nameVal,widgetId,sort)
            elif obj == "breedMenuEnt":
                self.entries[name] = formEntries.breedMenuEnt(self,nameVal,widgetId,sort)
            elif obj == "catHCMRECardiologicalAnalysisListBoxEnt":
                self.entries[name] = formEntries.catHCMRECardiologicalAnalysisListBoxEnt(self,nameVal,widgetId,sort)
            elif obj == "catKfCardiologicalAnalysisListBoxEnt":
                self.entries[name] = formEntries.catKfCardiologicalAnalysisListBoxEnt(self,nameVal,widgetId,sort)
            else:
                print("Error with widget ",obj)
            sort += 1
        self.inputFrame.pack()
        self.createScrollbar()
        self.createButtonFrame()



    def calcWeight(self,weight):
        indexes = self.master.getPetWeightIndex(self.pet)
        if weight <= indexes[0]:
            return "small"
        elif weight <= indexes[1]:
            return "average"
        else:
            return "tooMuch"

    def calcAge(self,age):
        indexes = self.master.getPetAgeIndex(self.pet)
        if age < indexes[0]:
            return "young"
        elif age < indexes[1]:
            return "adult"
        else:
            return "elder"

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
        self.mainFrame.destroy()
        self.master.checkState()

    def enterdata(self):
        filePath = self.master.path+"\\Protipa\\" + self.fileLocation
        doc = DocxTemplate(filePath)
        context = {}
        img = []


        self.loadingBar = ttk.Progressbar(self.buttonFrame, orient = "horizontal", length = 100, mode = 'determinate')
        self.loadingBar.pack(anchor = "s")

        loadingBarValue = 100/len(self.entries)
        for ent in self.entries:
            input = self.entries[ent].getWidgetValues()
            self.loadingBarProgress(loadingBarValue)

            if input == "" or input == "0.0" or input == [['', ' (0  )']] or input == None : # or ' (0.0 mg/kg po )'
                pass
            else:
                temp = []
                if ent == "PHOTOS":
                    for image in input:
                        myImage = InlineImage(doc, image, width = (5000),height = (5000))
                        temp.append(myImage)
                else:
                    temp = input
                context[ent] = temp


        doc.render(context)
        print(context)
        filePath = ""
        filePath = filedialog.asksaveasfilename(title = "Select file",filetypes = [("docx files","*.docx")])
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
