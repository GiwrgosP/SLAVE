import tkinter as tk
import db as db



class flowButtonEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.state = False
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.frames = list()
        self.buttonValue = list()
        self.widgets = list()
        self.widgetsInput = list()
        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def createWidgets(self):
        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)
        self.buttonValue.append(tk.StringVar())
        button = tk.Button(widgetFrame, text = self.text, command = self.buttonAction)
        self.widgets.append(button)
        self.widgetsInput .append(button)

        self.gridWidgets()
        widgetFrame.grid()

    def buttonAction(self):
        self.state = not self.state

        if self.state == True:
            self.buttonValue[0].set("Αντιστροφή διαμιτροειδικής ροής (Ε<Α κύμα), συμβατή με διαστολική δυσλειτουργία μυοκαρδίου.")
            self.widgetsInput[0].configure(bg = "red")
        else:
            self.buttonValue[0].set(" ")
            self.widgetsInput[0].configure(bg = "white")

    def getWidgetValues(self):
        return self.buttonValue[0].get()

    def gridWidgets(self):
        for ent in self.widgets:
            column = 0
            ent.grid(column = column, row = 0)
            column += 1

class ecgMenuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.frames = list()
        self.menuValue = list()
        self.widgets = list()
        self.widgetsInput = list()

        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def createWidgets(self):
        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)

        addButton = tk.Button(widgetFrame, text = "+", command = self.createWidgets)
        destroyButton = tk.Button(widgetFrame, text = "-", command = lambda x = widgetFrame: self.destroyButtonAction(x))

        values = db.getFieldValues(self.field,self.master.master.path)

        menuWidget = tk.Menubutton(widgetFrame, text = self.text)
        menuWidget.menu = tk.Menu(menuWidget)
        menuWidget["menu"] = menuWidget.menu

        temp = len(self.menuValue)
        self.menuValue.append(tk.StringVar())

        for val in values:
            menuWidget.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[temp])

        menuEntry = tk.Entry(widgetFrame, text = self.menuValue[temp])

        tempListWidgets = list()
        tempListWidgetsInput = list()

        tempListWidgets.append(addButton)
        tempListWidgets.append(destroyButton)

        tempListWidgets.append(menuWidget)

        tempListWidgets.append(menuEntry)
        tempListWidgetsInput.append(menuEntry)

        self.widgets.append(tempListWidgets)
        self.widgetsInput.append(tempListWidgetsInput)

        self.gridWidgets()
        widgetFrame.grid()

    def gridWidgets(self):
        for frame in self.widgets:
            column = 0
            for ent in frame:
                ent.grid(column = column, row = 0)
                column += 1

    def destroyButtonAction(self,frameForDel):
        if len(self.frames) == 1:
            print("no more frames available for delete")
        else:
            counter = 0
            for frame in self.frames:
                if frame == frameForDel:
                    break
                else:
                    counter += 1

            self.frames[counter].destroy()
            del self.frames[counter]
            del self.menuValue[counter]
            del self.widgets[counter]
            del self.widgetsInput[counter]

    def getWidgetValues(self):
        values = list()
        for ent in self.widgetsInput:
            groupValue = ent[0].get()
            values.append(groupValue)

        return values

class ageSpinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.value = tk.DoubleVar()
        self.radioButtonValue = tk.IntVar()
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()
        self.widgetsInput = list()

        spinBoxLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(spinBoxLabel)

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=1 ,command = lambda: self.giveValues())
        self.widgets.append(spinBoxWidget)
        self.widgetsInput.append(spinBoxWidget)

        radioButton1 = tk.Radiobutton(self.mainWidgetFrame, variable = self.radioButtonValue, text="Μηνών", value=1)
        self.widgets.append(radioButton1)
        self.widgetsInput.append(radioButton1)

        radioButton2 = tk.Radiobutton(self.mainWidgetFrame ,variable = self.radioButtonValue, text="Χρονών", value=2)
        radioButton2.select()
        self.widgets.append(radioButton2)
        self.widgetsInput.append(radioButton2)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)


    def checkSelf(self):
        pass

    def giveValues(self):
        spinBoxWeight = float(self.master.entries["weight"].widgetsInput[0].get())
        spinBoxAge = float(self.master.entries["age"].widgetsInput[0].get())

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

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        age = int(self.widgetsInput[0].get())
        timeAproximation = self.radioButtonValue.get()

        flagPlural = True
        if age == 1:
            flagPlural = False

        if timeAproximation == 2:
            textTimeAproximation = " χρονών"
            if flagPlural == False:
                textTimeAproximation = " έτους"
        else:
            textTimeAproximation = " μηνών"
            if flagPlural == False:
                textTimeAproximation = " μηνώς"

        return str(age) + textTimeAproximation

class medicMenuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.frames = list()
        self.menuValue = list()
        self.widgets = list()
        self.widgetsInput = list()

        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def createWidgets(self):
        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)

        addButton = tk.Button(widgetFrame, text = "+", command = self.createWidgets)
        destroyButton = tk.Button(widgetFrame, text = "-", command = lambda x = widgetFrame: self.destroyButtonAction(x))

        values = db.getFieldValues(self.field,self.master.master.path)

        menuWidget = tk.Menubutton(widgetFrame, text = self.text)
        menuWidget.menu = tk.Menu(menuWidget)
        menuWidget["menu"] = menuWidget.menu

        temp = len(self.menuValue)
        self.menuValue.append(tk.StringVar())

        for val in values:
            menuWidget.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[temp])

        menuEntry = tk.Entry(widgetFrame, text = self.menuValue[temp])

        spinBoxWidget = tk.Spinbox(widgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f")

        values3 = db.getFieldValues(25,self.master.master.path)

        menuWidget3 = tk.Menubutton(widgetFrame, text = "Μονάδα μέτρησης")
        menuWidget3.menu = tk.Menu(menuWidget3)
        menuWidget3["menu"] = menuWidget3.menu

        temp = len(self.menuValue)
        self.menuValue.append(tk.StringVar())

        for val in values3:
            menuWidget3.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[temp])

        menuEntry3 = tk.Entry(widgetFrame, text = self.menuValue[temp])

        values2 = db.getFieldValues(26,self.master.master.path)

        menuWidget2 = tk.Menubutton(widgetFrame, text = "Δοσολογία")
        menuWidget2.menu = tk.Menu(menuWidget2)
        menuWidget2["menu"] = menuWidget2.menu

        temp = len(self.menuValue)
        self.menuValue.append(tk.StringVar())

        for val in values2:
            menuWidget2.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[temp])

        menuEntry2 = tk.Entry(widgetFrame, text = self.menuValue[temp])

        tempListWidgets = list()
        tempListWidgetsInput = list()

        tempListWidgets.append(addButton)
        tempListWidgets.append(destroyButton)

        tempListWidgets.append(menuWidget)

        tempListWidgets.append(menuEntry)
        tempListWidgetsInput.append(menuEntry)

        tempListWidgets.append(spinBoxWidget)
        tempListWidgetsInput.append(spinBoxWidget)

        tempListWidgets.append(menuWidget3)

        tempListWidgets.append(menuEntry3)
        tempListWidgetsInput.append(menuEntry3)

        tempListWidgets.append(menuWidget2)

        tempListWidgets.append(menuEntry2)
        tempListWidgetsInput.append(menuEntry2)

        self.widgets.append(tempListWidgets)
        self.widgetsInput.append(tempListWidgetsInput)

        self.gridWidgets()
        widgetFrame.grid()

    def gridWidgets(self):

        for frame in self.widgets:
            column = 0
            for ent in frame:
                ent.grid(column = column, row = 0)
                column += 1

    def destroyButtonAction(self,frameForDel):
        if len(self.frames) == 1:
            print("no more frames available for delete")
        else:
            counter = 0
            for frame in self.frames:
                if frame == frameForDel:
                    break
                else:
                    counter += 1

            self.frames[counter].destroy()
            del self.frames[counter]
            del self.menuValue[counter]
            del self.widgets[counter]
            del self.widgetsInput[counter]

    def getWidgetValues(self):
        values = list()
        for ent in self.widgetsInput:
            groupValue = list()
            groupValue.append(ent[0].get())
            groupValue.append(" (" + ent[1].get() + " " + ent[2].get()+ " " + ent[3].get() + "), ")
            values.append(groupValue)

        values[-1][1] = values[-1][1][:-2]
        return values

class pdfReader(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]

        self.widgets = {}


        self.widgets["input"] = tk.Entry(self.master.inputFrame)
        #self.widgets["label"] = tk.Button(self.master.inputFrame, text = self.text, command = self.readPdf)

#    def readPdf(self):
#        pdfPath = self.widgets["input"].get() +"\\"+ "pdf.pdf"
#        with open(pdfPath, 'rb') as pdf:
#            pdf = open(pdfPath, mode = "rb")
#            pdfReader = PyPDF2.PdfFileReader(pdf)
#            page = pdfReader.getPage(0)
#            pdfText = page.extractText()
#            print("pppppppppppppppppp")
#            print(pdfText)
#            print("pppppppppppppppppp")

class menuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()
        self.widgetsInput = list()
        self.currentValue =  tk.StringVar()
        self.values = db.getFieldValues(self.field,self.master.master.path)

        menuWidget =  tk.Menubutton(self.mainWidgetFrame, text = self.text)
        self.widgets.append(menuWidget)

        self.applyValues()

        menuEntry = tk.Entry(self.mainWidgetFrame, text = self.currentValue)
        self.widgets.append(menuEntry)
        self.widgetsInput.append(menuEntry)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)


    def applyValues(self):
        self.widgets[0].menu =   tk.Menu(self.widgets[0])
        self.widgets[0]["menu"] = self.widgets[0].menu
        for val in self.values:
            self.widgets[0].menu.add_radiobutton(label = val[0], value = val[0],variable = self.currentValue)

    def checkSelf(self):
        flagFound = False
        value = self.currentValue.get()
        for ent in self.values:
            if value == ent[0]:
                flagFound = True
                break
        if flagFound == False:
            db.createFieldValue(self.master.master.path,value,self.field)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        return self.widgetsInput[0].get()


class spinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.value = tk.DoubleVar()
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()
        self.widgetsInput = list()

        spinBoxLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(spinBoxLabel)

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f")
        self.widgets.append(spinBoxWidget)
        self.widgetsInput.append(spinBoxWidget)

        self.individualize()

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)


    def individualize (self):
        if self.name == "weight" or self.name == "age":
            self.widgets[1].configure(command = lambda: self.giveValues())

    def checkSelf(self):
        pass

    def giveValues(self):
        spinBoxWeight = float(self.master.entries["weight"].widgetsInput[0].get())
        spinBoxAge = float(self.master.entries["age"].widgetsInput[0].get())

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

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = float(self.widgetsInput[0].get())
        if input % 1 == 0:
            input = int(input)
        return str(input)


class entryEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()
        self.widgetsInput = list()

        entryLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(entryLabel)

        entryWidget = tk.Entry(self.mainWidgetFrame)
        self.widgets.append(entryWidget)
        self.widgetsInput.append(entryWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def checkSelf(self):
        pass

    def getWidgetValues(self):
        return self.widgetsInput[0].get()
