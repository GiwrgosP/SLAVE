import tkinter as tk
from tkinter import messagebox
from docxtpl import DocxTemplate, InlineImage
from tkinter import filedialog
import widgets as formEntries
import tkinter.ttk as ttk

class formWindow(tk.Tk):
    #a dictionary of all the widgets and there objects
    #using a lambda function to call the creation of the objects
    widgetObjects = { \
    "menuEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.menuEnt(self,nameVal,name,widgetId,sort),\
    "entry" : lambda self,nameVal,name,widgetId,sort : formEntries.entryEnt(self,nameVal,name,widgetId,sort),\
    "mediMenu" : lambda self,nameVal,name,widgetId,sort : formEntries.medicMenuEnt(self,nameVal,name,widgetId,sort),\
    "ageSpinBoxEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.ageSpinBoxEnt(self,nameVal,name,widgetId,sort),\
    "ecgMenuEnt" :  lambda self,nameVal,name,widgetId,sort : formEntries.ecgMenuEnt(self,nameVal,name,widgetId,sort),\
    "flowButtonEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.flowButtonEnt(self,nameVal,name,widgetId,sort),\
    "checkUpSpinBoxEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.checkUpSpinBoxEnt(self,nameVal,name,widgetId,sort),\
    "nameAitEntryEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.nameAitEntryEnt(self,nameVal,name,widgetId,sort),\
    "bodyWeightSpinBoxEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.bodyWeightSpinBoxEnt(self,nameVal,name,widgetId,sort),\
    "dogDMVDCardiologicalAnalysisEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.dogDMVDCardiologicalAnalysisListBoxEnt(self,nameVal,name,widgetId,sort),\
    "weightSpinBoxEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.weightSpinBoxEnt(self,nameVal,name,widgetId,sort),\
    "pdfReader" : lambda self,nameVal,name,widgetId,sort : formEntries.pdfReader(self,nameVal,name,widgetId,sort),\
    "auditoryFindingsMenuEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.auditoryFindingsMenuEnt(self,nameVal,name,widgetId,sort),\
    "RECardiologicalAnalysisListBoxEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.dogDMVDRECardiologicalAnalysisListBoxEnt(self,nameVal,name,widgetId,sort),\
    "photoReader" : lambda self,nameVal,name,widgetId,sort : formEntries.photoReader(self,nameVal,name,widgetId,sort),\
    "historyMenuEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.historyMenuEnt(self,nameVal,name,widgetId,sort),\
    "breedMenuEnt" :  lambda self,nameVal,name,widgetId,sort : formEntries.breedMenuEnt(self,nameVal,name,widgetId,sort),\
    "catHCMRECardiologicalAnalysisListBoxEnt" : lambda self,nameVal,name,widgetId,sort : formEntries.catKfCardiologicalAnalysisListBoxEnt(self,nameVal,name,widgetId,sort)\
    }
    def __del__(self):
        print("Ending formsWindow")
        tempKeyList = list()


        print(self.entries)


    def __init__(self,master):
        #reference to window class as master
        self.master = master
        #reference to the id of the file -> form that has been selected to be filled
        self.fileId = self.master.fileSelected[0]
        #reference to the name of the file -> form that has been selected to be filled
        self.name = self.master.fileSelected[1]
        #reference to the language of the file -> form that has been selected to be filled
        self.language = self.master.fileSelected[2]
        #reference to the animal of the file -> form that has been selected to be filled
        self.pet = self.master.fileSelected[3]
        #reference to the file name(*.docx) of the file -> form that has been selected to be filled
        self.fileName = self.master.fileSelected[4]
        #reference to all the input widgets creted for this form
        self.entries = {}
        #a new frame inside the window class
        self.mainFrame = tk.Frame(self.master.window)
        #fill the mainFrame with the widgets for the file fileSelected
        self.createInputFrame()


        self.mainFrame.pack(fill = "both", expand = True)


    #open a list with widgets and constuct all them all
    def createInputFrame(self):
        #create a canvas to inside the mainFrame
        self.canvas = tk.Canvas(self.mainFrame)
        #create a frame inside the canvas
        self.inputFrame = tk.Frame(self.canvas, background = "bisque" )
        #call getForm(fileId) to get all the widgets specified for this file
        self.form = self.master.getForm(self.fileId)
        #for evety widget in the list create the object specified in the dictionary
        for widget in self.form:
            #
            obj,name,nameVal,sort = self.master.getWidget(widget)
            self.entries[name] = self.widgetObjects[obj](self,nameVal,name,widget,sort)

        self.inputFrame.pack()
        self.createButtonFrame()
        self.createScrollbar()

    #create a frame with utility buttons
    def createButtonFrame(self):
        #create a frame
        self.buttonFrame = tk.Frame(self.mainFrame)
        #create a label with the file's info (name language pet)
        self.fileSelectedLabel = tk.Label(self.buttonFrame, text = self.fileName + "\n" + self.language + "\n" + self.pet )
        self.fileSelectedLabel.pack(anchor = "n")
        #create a button to enter the informaton filled in the widgets
        self.enterData =  tk.Button(self.buttonFrame, text = "Enter Data", command = self.enterdata)
        self.enterData.pack(anchor = "center")
        #create a button to clear the information filled in the widgets
        self.clearButton =  tk.Button(self.buttonFrame, text = "Clear Form", command = self.clearForm)
        self.clearButton.pack(anchor = "center")
        #create a button to get back to the fileSelectionWindow
        self.quitButton =  tk.Button(self.buttonFrame, text="Back to form selection", command = self.quit)
        self.quitButton.pack(anchor = "s")

        self.buttonFrame.pack(side='right', fill = "y")
    #create a scroll bar inside the canvas and bind it to the mouse wheel
    def createScrollbar(self):
        self.canvas.update_idletasks()
        self.canvas.create_window(0, 0, anchor='nw', window=self.inputFrame)

        self.scrollBar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.scrollBar.pack(fill='y', side='right')

        self.canvas.configure(scrollregion=self.canvas.bbox('all'),yscrollcommand=self.scrollBar.set)
        #update the scrollbar place
        self.updateScrollBar()

        self.canvas.pack(fill='both', expand=True, side='left')

        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
    #update the scrollbar view
    def updateScrollBar(self):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'),yscrollcommand=self.scrollBar.set)
    #every mouse wheel bind for events
    def onMouseWheel(self, event):
        scrollDir = int(event.delta/120)
        self.canvas.yview('scroll',-1*scrollDir, "units")
        self.updateScrollBar()


    def clearForm(self):
        answer = messagebox.askyesno('You do not appreciate the work that your slave has done so far','Do you need slave to clear the board and start all over?')
        if answer:
            self.clearWidgets()

    def quit(self):
        answer = messagebox.askyesno('You need to your slave to hand an other task','Do you need slave to get you bask to the form selection window?')
        if answer:
            self.goBack()

    #to clear the widgets the canvas and the buttonFrame are destoyed and re-created
    def clearWidgets(self):
        self.canvas.destroy()
        self.buttonFrame.destroy()
        self.createInputFrame()

    #to get back to the fileSelectionWindow the fileSelected paremeter is equal to None
    #the mainFrame with the widgets is destroyed
    #and the function checkState is being called
    def goBack(self):
        self.master.fileSelected = None
        self.master.window.destroy()
        self.master.checkState()

    #a fuction to collect all the data from the widgets and create the docx file
    def enterdata(self):
        #get the string file path and name
        filePath = self.master.path+"\\Protipa\\" + self.fileName
        #make a DocxTemplate object
        doc = DocxTemplate(filePath)
        context = {}
        #make a loading bar into the buttonFrame
        self.loadingBar = ttk.Progressbar(self.buttonFrame, orient = "horizontal", length = 100, mode = 'determinate')
        self.loadingBar.pack(anchor = "s")
        #divide the progress bar into equal piecies, depending on the on many widget have been made
        loadingBarValue = 100/len(self.entries)
        #for every widget in the entries dictionary
        for ent in self.entries:
            #call the getWidgetValues function and store it in input
            input = self.entries[ent].getWidgetValues()
            #call the loadingBarProgress
            self.loadingBarProgress(loadingBarValue)

            if input == None :
                pass
            #if the there has been any change in the widgets
            else:
                #check in the input comes from the photo widget, in order to create an inlineinage object
                temp = []
                if ent == "PHOTOS":
                    for image in input:
                        myImage = InlineImage(doc, image, width = (5000),height = (5000))
                        temp.append(myImage)
                else:
                    temp = input
                #append the data from the input to the context dictionary
                context[ent] = temp

        #render the context dictionary
        doc.render(context)
        print(context)
        #clear the filePath paremeter
        filePath = ""
        #make a string of the path for the new to be saved at
        filePath = filedialog.asksaveasfilename(title = "Select file",filetypes = [("docx files","*.docx")])
        if filePath == "":
            #if the path is empty destroy the loading bar
            self.loadingBar.destroy()
        else:
            #add the .docx to the file
            filePath += ".docx"
            #save the file
            doc.save(filePath)
            #give the chose to go back to fileSelectionWindow or clear the widget at the forms window
            answer = messagebox.askyesno('Make slave keep working on this form','Whip slave and make him go back to work?')
            if answer:
                self.clearWidgets()
            else:
                self.goBack()

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

    def loadingBarProgress(self,val):
        self.loadingBar['value'] = self.loadingBar['value'] + val
        self.buttonFrame.update_idletasks()
