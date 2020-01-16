import tkinter as tk
import db as db
from tkinter import filedialog
import tika
from tika import parser
import re
from decimal import *

def buildNumber(num, formWindow):
    if num % 1 == 0:
        num = str(int(num))
    else:
        if num % 0.1 == 0:
            num = round(num,1)
        num = str(num)
        if formWindow.master.fileSelected[-1] == "greek":
            num = num.replace(".",",")

    return num

class auditoryFindingsMenuEnt(tk.Tk):
    systolic = ["ολοσυστολικό", "διαστολικό", "συνεχές"]
    degree = ["1ου βαθμού (1/6)", "2ου βαθμού (2/6)", "3ου βαθμού (3/6)", "4ου βαθμού (4/6)", "5ου βαθμού (5/6)", "6ου βαθμού (6/6)"]
    ausculation = ["αναγωγικού", "προωθητικού"]
    auditory = ["αριστερό", "δεξιό", "αριστερό και δεξιό"]
    heart = ["κορυφή", "βάση"]
    valve = ["μιτροειδούς", "τριγλώχινος", "πνευμονικής", "αορτικής"]

    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)

        self.menuValues = list()
        self.menuValues.append(self.systolic)
        self.menuValues.append(self.degree)
        self.menuValues.append(self.ausculation)
        self.menuValues.append(self.auditory)
        self.menuValues.append(self.heart)
        self.menuValues.append(self.valve)

        self.menuValue = list()

        self.widgets = list()

        widgetLabel = tk.Label(self.mainWidgetFrame, text = self.text )
        self.widgets.append(widgetLabel)

        self.menuValue.append(tk.StringVar(""))
        systolicMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "systolic")
        self.widgets.append(systolicMenuWidget)

        self.menuValue.append(tk.StringVar(""))
        degreeMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "degree")
        self.widgets.append(degreeMenuWidget)

        self.menuValue.append(tk.StringVar(""))
        ausculationMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "ausculation")
        self.widgets.append(ausculationMenuWidget)

        self.menuValue.append(tk.StringVar(""))
        auditoryMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "auditory")
        self.widgets.append(auditoryMenuWidget)

        self.menuValue.append(tk.StringVar(""))
        heartMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "heart")
        self.widgets.append(heartMenuWidget)

        self.menuValue.append(tk.StringVar(""))
        valveMenuWidget = tk.Menubutton(self.mainWidgetFrame, text = "valve")
        self.widgets.append(valveMenuWidget)

        self.applyValues()

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def getWidgetValues(self):
        input = list()
        for val in self.menuValue:
            temp = val.get()
            if temp != "":
                input.append(temp)
            else:
                return None
        return input[0] + ", " + input[1] + ", " + input[2] + \
        ", με σημείο αποκλειστικής ακροασιμότητας στο " + input[3] + \
        " ημιθωράκιο, στην " + input[4] + " της καρδιάς, στο ύψος της " \
        + input[5] + " βαλβίδας."

    def applyValues(self):
        for i in range(1,len(self.widgets[1:])+1):
            self.widgets[i].menu = tk.Menu(self.widgets[i])
            self.widgets[i]["menu"] = self.widgets[i].menu
            for val in self.menuValues[i-1]:
                self.widgets[i].menu.add_radiobutton(label = val, value = val,variable = self.menuValue[i-1])

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

class dogWeightSpinBoxEnt(tk.Tk):
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

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f",command = lambda: self.giveValues())
        self.widgets.append(spinBoxWidget)
        self.widgetsInput.append(spinBoxWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def giveValues(self):
        self.master.entries["cardiologicalAnalysis"].getMenuValues()

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = float(self.widgetsInput[0].get())
        return buildNumber(input,self.master)

class dogCardiologicalAnalysisListBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()
        self.widgetsInput = list()
        self.currentValue =  tk.StringVar("")

        menuWidget =  tk.Menubutton(self.mainWidgetFrame, text = self.text)
        self.widgets.append(menuWidget)

        menuEntry = tk.Entry(self.mainWidgetFrame, text = self.currentValue)
        self.widgets.append(menuEntry)
        self.widgetsInput.append(menuEntry)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def getMenuValues(self):
        spinBoxWeight = self.master.entries["weight"].getWidgetValues()
        spinBoxAge = self.master.entries["age"].getWidgetValues()
        spinBoxAge = spinBoxAge.split(" ")

        if spinBoxWeight != 0.00 and spinBoxWeight != None and spinBoxAge[0] != "0" :
            spinBoxWeight = spinBoxWeight.replace(",",".")


            if float(spinBoxWeight)<= 15.00:
                weight = "μικρόσωμο"
            elif float(spinBoxWeight) <= 55.00:
                weight = "μεγαλόσωμο"
            else:
                weight = "γιαγαντόσωμο"
            if spinBoxAge[1] != "μηνών" and spinBoxAge[1] != "μηνός":
                if int(spinBoxAge[0])<= 4:
                    age = "νεαρό"
                elif int(spinBoxAge[0]) <= 8:
                    age = "ενήλικο"
                else:
                    age = "υπερήλικο"
            else:
                age = "νεαρό"

            self.values = (("Καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο με υποψία καρδιακής νόσου.",),\
                                                ("Προεγχειρητικός καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",),\
                                                ("Προληπτικός καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",),\
                                                ("Προεγχειρητικός και προληπτικός  καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",))
            self.applyValues()
        else:
            pass

    def applyValues(self):
        self.widgets[0].menu =   tk.Menu(self.widgets[0])
        self.widgets[0]["menu"] = self.widgets[0].menu
        for val in self.values:
            self.widgets[0].menu.add_radiobutton(label = val[0], value = val[0],variable = self.currentValue)

    def checkSelf(self):
        pass

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = self.currentValue.get()
        if input == "":
            input == None
        else:
            self.checkSelf()
        return input

class bodyWeightSpinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()

        spinBoxLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(spinBoxLabel)

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0.5, to = 5, increment=0.5)
        self.widgets.append(spinBoxWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def getWidgetValues(self):
        num = float(self.widgets[1].get())
        if num < 1.5:
            input = "Καχεξία (BS: "
        elif num < 2.5:
            input = "Αδύνατο (BS: "
        elif num <= 4.0:
            input = "Κανονικό σωματικό βάρος (BS: "
        elif num <= 5:
            input = "Παχύσαρκο (BS: "

        temp = buildNumber(num, self.master)
        input += temp + "/5)"

        return input

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

class nameAitEntryEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()

        entryLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(entryLabel)

        entryWidget = tk.Entry(self.mainWidgetFrame)
        self.widgets.append(entryWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = self.widgets[1].get()
        if input == "":
            input = self.master.entries["petName"].getWidgetValues()
        return input

class checkUpSpinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()

        spinBoxLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(spinBoxLabel)

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=1)
        self.widgets.append(spinBoxWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def getWidgetValues(self):
        monthCounter = {
        1:"Ιανουάριος",\
        2:"Φεβρουάριος",\
        3:"Μάρτιος",\
        4:"Απρίλιος",\
        5:"Μάιος",\
        6:"Ιούνιος",\
        7:"Ιούλιος",\
        8:"Αύγουστος",\
        9:"Σεπτέμβριος",\
        10:"Οκτώβριος",\
        11:"Νοέμβριος",\
        12:"Δεκέμβριος"
        }
        input = list()
        curDate = self.master.entries["date"].getWidgetValues()
        if curDate!= None:
            curDate = curDate.split(".")

            curMonth = int(curDate[1])
            curYear = int(curDate[2])
            endDate = int(self.widgets[1].get())

            endMonth = monthCounter[(curMonth + endDate) % 12]
            endYear = (curMonth + endDate) // 12
            endYear+= curYear
            temp = list()
            temp.append(str(endDate))
            temp.append(endMonth)
            temp.append(str(endYear))
            input.append(temp)
        else:
            return None
        return input

    def checkSelf(self):
        pass

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

class flowButtonEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.state = False
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.buttonValue = tk.StringVar("")
        self.widgets = list()

        button = tk.Button(widgetFrame, text = self.text, command = self.buttonAction)
        self.widgets.append(button)

        self.gridWidgets()

        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def buttonAction(self):
        self.state = not self.state

        if self.state == True:
            self.buttonValue.set("Αντιστροφή διαμιτροειδικής ροής (Ε<Α κύμα), συμβατή με διαστολική δυσλειτουργία μυοκαρδίου.")
            self.widgets[0].configure(bg = "red")
        else:
            self.buttonValue.set("")
            self.widgets[0].configure(bg = "white")

    def getWidgetValues(self):
        input = self.buttonValue.get()
        if input == "":
            return None
        return input

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
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
        self.menuValues = list()
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
        self.menuValues.append(values)

        menuWidget = tk.Menubutton(widgetFrame, text = self.text)
        menuWidget.menu = tk.Menu(menuWidget)
        menuWidget["menu"] = menuWidget.menu

        self.menuValue.append(tk.StringVar(""))

        for val in values:
            menuWidget.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[-1])

        menuEntry = tk.Entry(widgetFrame, text = self.menuValue[-1])

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
        widgetFrame.grid(column = 0, row = len(self.frames)-1)

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
        for ent in self.menuValue:
            groupValue = ent.get()
            if groupValue == "":
                return None
            else:
                self.checkSelf()
                values.append(groupValue)
        return values

    def checkSelf(self):
        flagFound = False
        for i in range(len(self.menuValues)):
            for j in range(len(self.menuValues[i])):
                if self.menuValues[i][j] == self.menuValue[i].get():
                    flagFound = True
                    break
            if flagFound == False:
                db.createFieldValue(self.master.master.path,self.menuValue[i].get(),self.field)

# to giveValues na dinei sugkekrimenes times ston kardiologiko
class dogAgeSpinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
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

        radioButton2 = tk.Radiobutton(self.mainWidgetFrame ,variable = self.radioButtonValue, text="Ετών", value=2)
        radioButton2.select()
        self.widgets.append(radioButton2)
        self.widgetsInput.append(radioButton2)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)


    def checkSelf(self):
        pass

    def giveValues(self):
        self.master.entries["cardiologicalAnalysis"].getMenuValues()

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        age = int(self.widgetsInput[0].get())
        timeAproximation = self.radioButtonValue.get()

        flagPlural = True
        if age == 0:
            return None
        if age <= 1:
            flagPlural = False

        if timeAproximation == 2:
            textTimeAproximation = " ετών"
            if flagPlural == False:
                textTimeAproximation = " έτους"
        else:
            textTimeAproximation = " μηνών"
            if flagPlural == False:
                textTimeAproximation = " μηνός"

        return str(age)+textTimeAproximation

#Update
class medicMenuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.frames = list()
        self.menuValue = list()
        self.menuValues = list()
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
        self.menuValues.append(values)

        menuWidget = tk.Menubutton(widgetFrame, text = self.text)
        menuWidget.menu = tk.Menu(menuWidget)
        menuWidget["menu"] = menuWidget.menu

        self.menuValue.append(tk.StringVar(""))

        for val in values:
            menuWidget.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[-1])

        menuEntry = tk.Entry(widgetFrame, text = self.menuValue[-1])

        spinBoxWidget = tk.Spinbox(widgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f")

        values = db.getFieldValues(25,self.master.master.path)
        self.menuValues.append(values)

        menuWidget3 = tk.Menubutton(widgetFrame, text = "Μονάδα μέτρησης")
        menuWidget3.menu = tk.Menu(menuWidget3)
        menuWidget3["menu"] = menuWidget3.menu

        self.menuValue.append(tk.StringVar(""))

        for val in values:
            menuWidget3.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[-1])

        menuEntry3 = tk.Entry(widgetFrame, text = self.menuValue[-1])

        values = db.getFieldValues(26,self.master.master.path)
        self.menuValues.append(values)

        menuWidget2 = tk.Menubutton(widgetFrame, text = "Δοσολογία")
        menuWidget2.menu = tk.Menu(menuWidget2)
        menuWidget2["menu"] = menuWidget2.menu

        self.menuValue.append(tk.StringVar(""))

        for val in values:
            menuWidget2.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[-1])

        menuEntry2 = tk.Entry(widgetFrame, text = self.menuValue[-1])

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
        widgetFrame.grid(column = 0, row = 0)

    #pass
    def applyValues():
        pass

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
            if ent[0].get() != "ουδεμία" and ent[0].get() != "δεν συστήνεται":
                num = buildNumber(float(ent[1].get()),self.master)
                groupValue.append(" (" + num + " " + ent[2].get()+ " " + ent[3].get() + "), ")
                values.append(groupValue)
            else:
                return None
        values[-1][1] = values[-1][1][:-2]

        self.checkSelf()
        return values

    def checkSelf(self):
        flagFound = False
        for i in range(len(self.menuValues)):
            for j in range(len(self.menuValues[i])):
                if self.menuValues[i][j] == self.menuValue[i].get() or self.menuValue[i].get() == "" :
                    flagFound = True
                    j = len(self.menuValues[i])-1

            if flagFound == False:
                if i == 0:
                    field = self.field
                elif i == 1:
                    field == 25
                else:
                    field == 26
                db.createFieldValue(self.master.master.path,self.menuValue[i].get(),field)

class pdfReader(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.currentValue =  tk.StringVar("")
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()

        button = tk.Button(self.mainWidgetFrame, text = self.text, command = self.buttonAction)
        self.widgets.append(button)

        buttonEntry = tk.Entry(self.mainWidgetFrame, text = self.currentValue, state = 'disabled' )
        self.widgets.append(buttonEntry)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)


    def buttonAction(self):
        fileName = filedialog.askopenfilename(filetypes = (("pdf files","*.pdf"),))
        self.currentValue.set(fileName)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        fileName = self.currentValue.get()
        if fileName == "":
            return None
        else:
            tags = db.getEksetasi(self.master.master.path)
            parsed = parser.from_file(fileName)
            tempDoc = parsed["content"].split("Status:")
            tempDoc = tempDoc[0].split("M\xadMode")
            tempDoc = re.sub("\n", " ", tempDoc[1])
            tempDoc = tempDoc.split(" ")
            doc = list()
            result = {}
            for i in tempDoc:
                doc.append(re.sub("\xa0", " ", i))
            for tag in tags:
                for i in range(len(doc)):
                    if tag[0] == doc[i]:
                        temp = list()
                        for j in range(1,tag[2]+1):
                            temp.append(re.sub("\xad", "",doc[i+j]))
                        result[tag[1]] = temp
                        break

            input = {}
            for i in result:
                if len(result[i])==2 and result[i][1] == "cm":
                    temp = float(Decimal(result[i][0]) * Decimal(10))
                else:
                    temp = float(result[i][0])

                input[i] = buildNumber(temp,self.master)

        return input

class menuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()
        self.currentValue =  tk.StringVar("")
        self.values = db.getFieldValues(self.field,self.master.master.path)

        menuWidget =  tk.Menubutton(self.mainWidgetFrame, text = self.text)
        self.widgets.append(menuWidget)
        self.applyValues()

        menuEntry = tk.Entry(self.mainWidgetFrame, text = self.currentValue)
        self.widgets.append(menuEntry)

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
        if self.currentValue.get() == "":
            return None
        else:
            self.checkSelf()
            return self.currentValue.get()

class spinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()
        self.widgetsInput = list()

        spinBoxLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(spinBoxLabel)

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f")
        self.widgets.append(spinBoxWidget)
        self.widgetsInput.append(spinBoxWidget)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        input = float(self.widgetsInput[0].get())
        return buildNumber(input,self.master)

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

    def getWidgetValues(self):
        input = self.widgetsInput[0].get()
        if input == "":
            input = None
        return input
