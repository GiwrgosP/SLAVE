import tkinter as tk
from tkinter import filedialog
import tika
from tika import parser
import re
from decimal import *
import glob
import os
from PIL import Image

def resizeImage(images):
    resizedImageList = list()
    for img in images:
        temp = Image.open(img)
        str = img[:-4]
        resizeImage = temp.resize((430,404))
        resizeImage.save(str+"resized.bmp")
        resizedImageList.append(str+"resized.bmp")
    return resizedImageList



def replaceValues(values,value):
    result = list()
    for sentence in values:
        temp = sentence
        for word in value:
            temp = temp.replace(word[::-1],value[word].get())

        result.append(temp)
    return result

def indexDoc(doc,tagList):
    indexList = list()
    stringList = {}
    for tag in tagList:
        try:
            startIndex = doc.index(tag)
        except ValueError:
            pass
        else:
            endIndex = startIndex+len(tag)

            indexList.append((startIndex,endIndex))

    indexList = sorted(indexList, key = lambda x : x[1])
    endIndex = len(doc)

    for i in range(len(indexList)-1,-1,-1):
        stringList[doc[indexList[i][0]:indexList[i][1]]] = doc[indexList[i][1]:endIndex]
        endIndex = indexList[i][0]
    return stringList

def buildNumber(num, formWindow):
    if num % 1 == 0:
        num = str(int(num))
    else:
        if num % 0.1 == 0:
            num = round(num,1)
        num = str(num)
        if formWindow.master.fileSelected[2] == "greek":
            num = num.replace(".",",")
    return num

def replaceValues(values,value):
    result = list()
    for sentence in values:
        temp = sentence
        for word in value:
            temp = temp.replace(word[::-1],value[word].get())

        result.append(temp)

    return result

def frameBgColor(ent):
    if ent == 0:
        return "sky blue"
    else:
        if ent % 2 == 0:
            return "sky blue"
        else:
            return "light cyan"
#a fuction to frid all widgets
def gridWidgets(widgets):
    column = 0
    for ent in widgets:
        ent.grid(column = column, row = 0)
        column += 1

#a fuction to fill a menu with its values and link it to a string Var
def fillMenuWithValues(menuObj,values,variable):
    menuObj.menu = tk.Menu(menuObj)
    menuObj["menu"] = menuObj.menu
    #add a default value to the menu "+++"
    menuObj.menu.add_radiobutton(label = "+++", value = "+++",variable = variable)
    #add all the value, from the menuValues list to the menu and bind them to the string var at self.value
    for val in values:
        menuObj.menu.add_radiobutton(label = val, value = val, variable = variable)


#widget having a frame with a label and an entry
class entryEnt(tk.Tk):

    def __del__(self):
        print("hello")
        val = self.getWidgetValues()


    def __init__(self, master,nameVal, name, widgetId, sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and a string Var
        #so that the value can be accesed by a different object
        self.value = { self.widgetId : tk.StringVar(value="+++")}
        #a list with all the widgets of this object
        self.widgets = list()

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))

        self.widgets.append(tk.Label(self.frame, text = self.displayName))
        self.widgets.append(tk.Entry(self.frame, textvariable = self.value[self.widgetId]))
        #call the function gridWidgets to grid the widgets in the widget list
        gridWidgets(self.widgets)

        self.frame.grid(column = 0, row = self.sort, sticky = "we", padx = 5, pady = 5)

    #chech if the value has been altered in a meaningful way
    #return the value or None
    def getWidgetValues(self):
        value = self.value[self.widgetId].get()
        if value != "+++" and len(value.split()) != 0:
            return value
        return None

#widget having a frame with a menu, entry and a label
class menuEnt(tk.Tk):
    def __init__(self, master, nameVal, name, widgetId, sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and a string Var
        #so that the value can be accesed by a different object
        self.value = { self.widgetId : tk.StringVar(value="+++")}
        #a list with all the widgets of this object
        self.widgets = list()
        #call to the window object in order to get the menuId for the widget
        self.menuId = self.master.master.getWidgetMenuId(self.widgetId)
        #call to the window object to get a list of the menuValues for the menu
        self.menuValues = self.master.master.getValues(self.menuId[0])

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        #make a menu widget and add it to the widgets list
        self.widgets.append(tk.Menubutton(self.frame, text = self.displayName))

        fillMenuWithValues(self.widgets[0],self.menuValues,self.value[self.widgetId])
        #make an entry widgets that shows the string var from the self.value
        self.widgets.append( tk.Entry(self.frame, text = self.value[self.widgetId]))

        #call the function gridWidgets to grid the widgets in the widget list
        gridWidgets(self.widgets)

        self.frame.grid(column = 0, row = self.sort, sticky = "we", padx = 5, pady = 5)

    #a function to look if the value submited in the entry widget existied in the menuValues list
    def checkSelf(self):
        if self.menuValues.count(self.value[self.widgetId].get()) == 0 :
            self.master.master.createValue(self.value[self.widgetId].get(),self.menuId[0])
    #chech if the value has been altered in a meaningful way
    #return the value and chech if the value exists on the menu value list or return None
    def getWidgetValues(self):
        value = self.value[self.widgetId].get()
        if value != "+++" and len(value.split()) != 0:
            self.checkSelf()
            return value
        return None

#widget having a frame with addable and removable frames inside
#each sub-frame has buttons to add or remove and a label
#also each subframe has menus with corresponding labels and entries and a spinbox
class medicMenuEnt(tk.Tk):
    def __init__(self, master,nameVal, name, widgetId, sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and a string Var of all the inputs for this objet
        #so that the value can be accesed by a different object
        self.value = {}
        #a dictionary with the widgetId and a list of all the menus for this object
        self.menuValues = {}
        #a list with all the widgets of this object
        self.widgets = list()
        #a list with the frames that have been created
        self.frames = list()

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        #call to the window object in order to get the menuId for the widget
        #a list of all the menus for this widget
        self.menuId = self.master.master.getWidgetMenuId(self.widgetId)
        #for every menu in the list
        for menu in self.menuId:
            #create a list that will contain all the values for this menu
            #this widget can have more than one of each menu
            self.value[menu] = list()
            #call the getValues fuction to collect all the values for this menu
            self.menuValues[menu] = self.master.master.getValues(menu)

        self.value["doseNumber"] = list()
        self.createWidgets()
        self.frame.grid(column = 0, row = self.sort, sticky = "we", padx = 5, pady = 5)

    def createWidgets(self):
            #a temp frame
            tempFrame = tk.Frame(self.frame)
            #a temporary list with all the widgets for this frame
            tempWidgetList = list()
            #a button that calls this fuction to create a new frame
            tempWidgetList.append(tk.Button(tempFrame, text = "+", command = self.createWidgets))
            #a button that destroys this frame and its data
            tempWidgetList.append(tk.Button(tempFrame, text = "-", command = lambda x = tempFrame: self.destroyButtonAction(x)))
            #a label with the self.display name
            tempWidgetList.append(tk.Button(tk.Label(tempFrame, text = self.displayName)))
            #for every menu in the self.menuValues list
            for menu in self.menuValues:
                #create a menu
                tempWidgetList.append(tk.Menubutton(tempFrame, text = menu))
                #create a string Var
                self.value[menu].append(tk.StringVar(value = "+++"))
                #call the function fillMenuWithValues
                fillMenuWithValues(tempWidgetList[-1],self.menuValues[menu],self.value[menu][-1])
                #make an entry for the menu
                tempWidgetList.append(tk.Entry(tempFrame, textvariable = self.value[menu][-1]))

                if menu == "medicationGreekMenu" or menu == "medication2GreekMenu":
                    self.value["doseNumber"].append(tk.StringVar(value = "0.0"))
                    tempWidgetList.append(tk.Spinbox(tempFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f",textvariable = self.value["doseNumber"][-1]))

            self.frames.append(tempFrame)
            self.widgets.append(tempWidgetList)
            gridWidgets(tempWidgetList)
            tempFrame.grid(column = 0, row = len(self.widgets)-1)

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

            for menu in self.values:
                del self.value[menu][counter]

            del self.widgets[counter]

    def getWidgetValues(self):
        #a list for all the valid values of this widget
        values = list()
        #a counter for all the frames that have been made for this widget
        counter = len(self.widgets)
        #a simpe flag to
        flag = True
        #for all the frames
        for i in range(counter):
            #a temp dictionary to store all the values of the frame
            temp = {}
            #for all the widgets in the dictionary self.value
            for menu in self.value:
                #store all the values from the widgets of this frame into temp
                temp[menu] = self.value[menu][i].get()
            #check if all the values from the widgets in this frame have been altered in any way
            for t in temp:
                #in any of them is not valid make the flag false
                if temp[t] == "+++" or temp[t] == "0.0" or len(temp[t].split()) == 0:
                    flag = False

            #if all the values are valid
            if flag == True:
                #call the function buildNumber for the dose number
                temp["doseNumber"] = buildNumber(float(temp["doseNumber"]),self.master)
                #save temp to values
                values.append(temp)
                #check if the values of the menus in temp are are new or existed
                self.checkSelf(temp)
        #if values list is not empty return it else return None
        if len(values) != 0:
            return values
        else:
            return None
    #check if the values of the from the widgets of a frame are new and add them on the database
    def checkSelf(self,value):
        for menu in self.menuValues:
            if self.menuValues[menu].count(value[menu]) == 0:
                self.master.master.createValue(value[menu],menu)

#widgets having a frame with a label, spinbox and wo radiobuttons
#using the age and the selection of the radiobuttons to add a string to the widgets value
class ageSpinBoxEnt(tk.Tk):
    def __init__(self, master, name, nameVal, widgetId, sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and a string Var for the number of age
        #and an IntVar for the ageAproximaton (e.g ετών, μηνών)
        #so that the value can be accesed by a different object
        self.value = { "age" : tk.IntVar(value = 0), "ageAprox" : tk.IntVar(value = 2)}
        #a list with all the widgets of this object
        self.widgets = list()

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))

        self.widgets.append(tk.Label(self.frame, text = self.displayName))
        self.widgets.append(tk.Spinbox(self.frame, from_ = 0, to = 1000, increment= 1,textvariable = self.value["age"]))

        self.widgets.append(tk.Radiobutton(self.frame, variable = self.value["ageAprox"], text="Μηνών",value = 1))
        self.widgets.append(tk.Radiobutton(self.frame, variable = self.value["ageAprox"], text="Ετών", value = 2))
        #make the last radiobutton the default selection
        self.widgets[-1].select()

        gridWidgets(self.widgets)
        self.frame.grid(column = 0, row =self.sort,sticky = "we",padx = 5, pady = 5)

    def getWidgetValues(self):
        age = self.value["age"].get()
        timeAproximation = self.value["ageAprox"].get()

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

#widget having a frame with a label, a button and an entryEnt
#reading a pdf file to get its data
class pdfReader(tk.Tk):
    def __init__(self, master, nameVal,name ,widgetId ,sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and a string Var of all the inputs for this objet
        #so that the value can be accesed by a different object
        self.value = {self.widgetId : tk.StringVar(value = "+++")}
        #a dictionary with the widgetId and a list of all the menus for this object
        self.menuValues = {}
        #a list with all the widgets of this object
        self.widgets = list()
        #a list with the frames that have been created
        self.frames = list()

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))

        self.widgets.append(tk.Label(self.frame, text = self.displayName))
        self.widgets.append(tk.Button(self.frame, text = "Select", command = self.buttonAction))
        self.widgets.append(tk.Entry(self.frame, text = self.value[self.widgetId], state = 'disabled' ))

        gridWidgets(self.widgets)

        self.frame.grid(column = 0, row = self.sort, sticky = "we", padx = 5, pady = 5)


    #asking the user to point to a pdf file
    #if the file directs exixts
    def buttonAction(self):
        fileName = filedialog.askopenfilename(filetypes = (("pdf files","*.pdf"),))
        #if the file directs exixts
        if os.path.exists(fileName):
            #save the path and file name to the string Var
            self.value[self.widgetId].set(fileName)
        else:
            pass

    def getWidgetValues(self):
        fileName = self.value[self.widgetId].get()
        if fileName == "+++":
            return None
        else:
            catDataList = self.master.master.getThema()

            tags = list()
            tempTags = self.master.master.getEksetasi()
            for i in tempTags:
                tags.append(i[0])

            parsed = parser.from_file(fileName)
            metaData = parsed["metadata"]
            doc = parsed["content"]
            doc = re.sub("\n", " ", doc)

            thema = indexDoc(doc,catDataList)

            catData = {}
            for i in thema:
                catData[i] = indexDoc(thema[i],self.master.master.getCategory(i))


            titlesData = {}
            titlesList = self.master.master.getTitles("Cardio Canine")
            for cat in catData["Cardio Canine"]:
                titlesData[cat] = indexDoc(catData["Cardio Canine"][cat],titlesList)

            tempTitles = {}
            for i in titlesData:
                tempTitles[i] = {}
                for j in titlesData[i]:
                    tempTitles[i][j] = indexDoc(titlesData[i][j],tags)

            cardioCanine = {}
            for cat in tempTitles:
                for title in tempTitles[cat]:
                    for tag in tempTitles[cat][title]:
                        if tag not in cardioCanine:
                            cardioCanine[tag] = tempTitles[cat][title][tag].split()

            for i in cardioCanine:
                if "cm" in cardioCanine[i][1:]:
                    temp = float(Decimal(cardioCanine[i][0]) * Decimal(10))
                else:
                    if len(cardioCanine[i])!=0:
                        temp = float(cardioCanine[i][0])
                cardioCanine[i] = buildNumber(temp,self.master)

            input = {}
            for tag in tempTags:
                try:
                     if "-" not in cardioCanine[tag[0]]:
                         temp = cardioCanine[tag[0]]
                     else:
                         temp = cardioCanine[tag[0]].replace("-","")
                     input[tag[2]] = temp
                except:
                    pass

        return input

#like medimenuent
class ecgMenuEnt(tk.Tk):
    def __init__(self, master, nameVal, name, widgetId, sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and a string Var of all the inputs for this objet
        #so that the value can be accesed by a different object
        self.value = {self.widgetId : list() }
        #a dictionary with the widgetId and a list of all the menus for this object
        self.menuValues = {}
        #a list with all the widgets of this object
        self.widgets = list()
        #a list with the frames that have been created
        self.frames = list()

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        #call to the window object in order to get the menuId for the widget
        #a list of all the menus for this widget
        self.menuId = self.master.master.getWidgetMenuId(self.widgetId)
        self.menuValues = self.master.master.getValues(self.menuId[0])

        self.createWidgets()
        self.frame.grid(column = 0, row = self.sort, sticky = "we", padx = 5, pady = 5)

    def createWidgets(self):
            #a temp frame
            tempFrame = tk.Frame(self.frame)
            #a temporary list with all the widgets for this frame
            tempWidgetList = list()
            #a button that calls this fuction to create a new frame
            tempWidgetList.append(tk.Button(tempFrame, text = "+", command = self.createWidgets))
            #a button that destroys this frame and its data
            tempWidgetList.append(tk.Button(tempFrame, text = "-", command = lambda x = tempFrame: self.destroyButtonAction(x)))
            #a label with the self.display name
            tempWidgetList.append(tk.Button(tk.Label(tempFrame, text = self.displayName)))

            #create a menu
            tempWidgetList.append(tk.Menubutton(tempFrame, text =self.displayName))
            #create a string Var
            self.value[self.widgetId].append(tk.StringVar(value = "+++"))
            #call the function fillMenuWithValues
            fillMenuWithValues(tempWidgetList[-1],self.menuValues,self.value[self.widgetId][-1])
            #make an entry for the menu
            tempWidgetList.append(tk.Entry(tempFrame, textvariable = self.value[self.widgetId][-1]))

            self.frames.append(tempFrame)
            self.widgets.append(tempWidgetList)
            gridWidgets(tempWidgetList)
            tempFrame.grid(column = 0, row = len(self.widgets)-1)

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

            for menu in self.values:
                del self.value[counter]

            del self.widgets[counter]

    def getWidgetValues(self):
        #a list for all the valid values of this widget
        values = list()
        #a counter for all the frames that have been made for this widget
        counter = len(self.widgets)
        #a simpe flag to
        flag = True
        #for all the frames
        for i in range(counter):
            val = self.value[self.widgetId][i].get()
            if val == "+++" or len(val.split()) == 0:
                pass
            else:
                values.append(val)
                self.checkSelf(val)
        #if values list is not empty return it else return None
        if len(values) != 0:
            return values
        else:
            return None
    #check if the values of the from the widgets of a frame are new and add them on the database
    def checkSelf(self,value):
        if self.menuValues.count(value) == 0:
            self.master.master.createValue(value,self.menuId[0])

#like entry but with a trace call on petName to much it when it is changed
class nameAitEntryEnt(tk.Tk):
    def __init__(self, master, nameVal, name, widgetId, sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and a string Var
        #so that the value can be accesed by a different object
        self.value = { self.widgetId : tk.StringVar(value="+++")}
        #a list with all the widgets of this object
        self.widgets = list()

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))

        self.widgets.append(tk.Label(self.frame, text = self.displayName))
        self.widgets.append(tk.Entry(self.frame, textvariable = self.value[self.widgetId]))
        #call the function gridWidgets to grid the widgets in the widget list
        gridWidgets(self.widgets)

        self.frame.grid(column = 0, row = self.sort, sticky = "we", padx = 5, pady = 5)

        self.tracePetname()


    def tracePetname(self):
        try:
            self.master.entries["petName"].value["petName"].trace_add("write", self.updateValue)
        except:
            pass

    def updateValue(self, *args):
        self.value[self.widgetId].set(self.master.entries["petName"].value["petName"].get())

    def getWidgetValues(self):
        value = self.value[self.widgetId].get()
        if value != "+++" and len(value.split()) != 0:
            return value
        return None

#widget having frame with a label and a Spinbox
#and culculates a date based on date widgets and its value
class checkUpSpinBoxEnt(tk.Tk):
    monthCounter = { 1:"Ιανουάριος",\
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
    12:"Δεκέμβριος"}

    def __init__(self, master, name, nameVal, widgetId, sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and an Intvar
        #so that the value can be accesed by a different object
        self.value = { self.widgetId : tk.IntVar(value = 0)}
        #a list with all the widgets of this object
        self.widgets = list()

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))

        self.widgets.append(tk.Label(self.frame, text = self.displayName))
        self.widgets.append(tk.Spinbox(self.frame, from_ = 0, to = 1000, increment= 1,textvariable = self.value[self.widgetId]))

        gridWidgets(self.widgets)
        self.frame.grid(column = 0, row =self.sort,sticky = "we",padx = 5, pady = 5)

    def getWidgetValues(self):
        try:
            #try to get the value of the date widget
            curDate = self.master.entries["date"].value["date"].get()
        except:
            pass
        else:
            #if it exists
            nextVisitMonths = self.value[self.widgetId].get()
            #if the date values is altered and this widgets has been altered
            if curDate != "+++" and nextVisitMonths != 0:
                #split the date value by "."
                curDate = curDate.split(".")
                #divide the values of the paremeter
                curMonth = int(curDate[1])
                curYear = int(curDate[2])
                #make a paremeter of the sum between current month and the mothns for next visit
                temp = nextVisitMonths + curMonth
                #pick a month with the mothcounter dictionary
                if temp > 12:
                    endMonth = self.monthCounter[temp % 12]
                    #calculate the year
                    endYear = curYear + (temp // 12)
                else:
                    endMonth = temp
                    endYear = curYear
                return [[str(nextVisitMonths),endMonth,str(endYear)]]

            else:
                return None

#
class bodyWeightSpinBoxEnt(tk.Tk):
    def __init__(self, master, name, nameVal, widgetId, sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and a string Var for the number of age
        #and an IntVar for the ageAproximaton (e.g ετών, μηνών)
        #so that the value can be accesed by a different object
        self.value = { self.widgetId : tk.DoubleVar()}
        #call to the window object in order to get the menuId for the widget
        self.menuId = self.master.master.getWidgetMenuId(self.widgetId)
        #call to the window object to get a list of the menuValues for the menu
        self.menuValues = self.master.master.getValues(self.menuId)
        #a list with all the widgets of this object
        self.widgets = list()

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))

        self.widgets.append(tk.Label(self.frame, text = self.displayName))
        self.widgets.append(tk.Spinbox(self.frame, from_ = 0, to = 5, increment=1,textvariable = self.value[self.widgetId]))

        gridWidgets(self.widgets)
        self.frame.grid(column = 0, row =self.sort,sticky = "we",padx = 5, pady = 5)

    def getWidgetValues(self):
        num = self.value[self.widgetId].get()

        if num == 1.5:
            return None
        elif num <  1.5:
            input = self.menuValues[1]
        elif num <= 2.5:
            input = self.menuValues[1]
        elif num <= 4.0:
            input = self.menuValues[2]
        elif num <= 5:
            input = self.menuValues[3]
        else:
            print("Error with widget ", self.name, num)
            return None

        temp = buildNumber(num,self.master)
        input += temp + "/5)"

        return input

#
class weightSpinBoxEnt(tk.Tk):
    def __init__(self, master, name, nameVal, widgetId, sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and a string Var for the number of age
        #and an IntVar for the ageAproximaton (e.g ετών, μηνών)
        #so that the value can be accesed by a different object
        self.value = { self.widgetId : tk.DoubleVar()}
        #a list with all the widgets of this object
        self.widgets = list()

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))

        self.widgets.append(tk.Label(self.frame, text = self.displayName))
        self.widgets.append(tk.Spinbox(self.frame, from_ = 0, to = 1000, increment=0.1, format= "%.1f", textvariable = self.value[self.widgetId]))

        gridWidgets(self.widgets)
        self.frame.grid(column = 0, row =self.sort,sticky = "we",padx = 5, pady = 5)

    def getWidgetValues(self):
        num = self.value[self.widgetId].get()
        if num == 0.0:
            return None
        return buildNumber(num,self.master)

#
class dogDMVDCardiologicalAnalysisListBoxEnt(tk.Tk):
    fileStructAge = { "greek" : {"young" : "νεαρό", "adult" : "ενήλικο", "elder" : "υπερήλικο"},\
                        "english" : { "young" : "young", "adult" : "adult", "elder" : "elder"}}

    fileStructWeight = { "greek" : { "small" : "μικρόσωμο", "average" : "μεγαλόσωμο", "υπέρβαρο" : "huge"},\
                            "english" : {  "small" : "small", "average" : "average", "tooMuch" : "huge"}}
    def __init__(self, master,nameVal, name, widgetId, sort):
        #reference to formWinfow Object
        self.master = master
        #the name to be displayed by the Label widget
        self.displayName = nameVal
        #reference to for the value of this object
        self.widgetId = widgetId
        #row of the widget to be grided when displayed
        self.sort = sort
        #a dictionary with the widgetId and a string Var
        #so that the value can be accesed by a different object
        self.value = { "weight" : tk.StringVar(value = "+++"), "age" : tk.StringVar(value = "+++"), self.widgetId : tk.StringVar(value = "")}
        #a list with all the widgets of this object
        self.widgets = list()

        self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))
        self.widgets.append(tk.Entry(self.frame, text = self.value[self.widgetId], state = 'disabled' ))
        self.widgets.append(tk.Menubutton(self.frame, text = self.displayName))



        self.master.entries["weight"].value["weight"].trace_add("write",  self.updateValueWeight)
        self.master.entries["age"].value["age"].trace_add("write", self.updateValueAge)
        self.master.entries["age"].value["ageAprox"].trace_add("write", self.updateValueAge)


        gridWidgets(self.widgets)
        self.frame.grid(column = 0, row = self.sort, sticky = "we", padx = 5, pady = 5)


    def updateState(self):
        if self.value["weight"].get() == "+++" or self.value["age"].get() == "+++":
            self.widgets[-1].configure(state = "disabled")
        else:
            self.widgets[-1].configure(state = "normal")
            self.applyValues()

    def applyValues(self):
        try:
            self.widgets[1].menu.destroy()
        except:
            pass
        self.values = replaceValues(self.master.master.getValues(self.master.master.getWidgetMenuId(self.widgetId)[0]),self.value)

        self.widgets[1].menu =   tk.Menu(self.widgets[1])
        self.widgets[1]["menu"] = self.widgets[1].menu
        self.widgets[1].menu.add_radiobutton(label = "+++", value ="+++",variable = self.value[self.widgetId])

        for val in self.values:
            self.widgets[1].menu.add_radiobutton(label = val, value = val,variable = self.value[self.widgetId])

    def updateValueWeight(self, *args):
        try:
            val = self.master.entries["weight"].value["weight"].get()
        except:
            pass
        else:
            if val != 0.0:
                weight = float(val)
                temp = self.fileStructWeight[self.master.language][self.master.calcWeight(weight)]
            else:
                temp = "+++"

        self.value["weight"].set(temp)
        self.updateState()

    def updateValueAge(self, *args):
        try:
            age = self.master.entries["age"].value["age"].get()
        except:
            pass
        else:
            approx = self.master.entries["age"].value["ageAprox"].get()

            if approx == 1:
                temp = self.fileStructAge[self.master.language]["young"]
            else:
                if age == 0:
                    temp = "+++"
                else:
                    temp = self.fileStructAge[self.master.language][self.master.calcAge(age)]

            self.value["age"].set(temp)

            self.updateState()

    def getWidgetValues(self):
        input = self.value[self.widgetId].get()
        if input == "+++" or input == "":
            return None
        return input

class photoReader(tk.Tk):
        def __init__(self, master, nameVal,name ,widgetId ,sort):
            #reference to formWinfow Object
            self.master = master
            #the name to be displayed by the Label widget
            self.displayName = nameVal
            #reference to for the value of this object
            self.widgetId = widgetId
            #row of the widget to be grided when displayed
            self.sort = sort
            #a dictionary with the widgetId and a string Var of all the inputs for this objet
            #so that the value can be accesed by a different object
            self.value = {self.widgetId : tk.StringVar(value = "+++")}
            #a list with all the widgets of this object
            self.widgets = list()


            self.frame = tk.Frame(self.master.inputFrame, background = frameBgColor(self.sort))

            self.widgets.append(tk.Label(self.frame, text = self.displayName))
            self.widgets.append(tk.Button(self.frame, text = "Select", command = self.buttonAction))
            self.widgets.append(tk.Entry(self.frame, text = self.value[self.widgetId], state = 'disabled' ))

            gridWidgets(self.widgets)

            self.frame.grid(column = 0, row = self.sort, sticky = "we", padx = 5, pady = 5)

        def buttonAction(self):
            filePath = filedialog.askdirectory()
            import os
            if filePath != None:
                self.value[self.widgetId].set(filePath)
            else:
                pass

        def getWidgetValues(self):
            val = self.value[self.widgetId].get()
            if val != "+++" and val != "":
                images = glob.glob(str(val)+"/*.bmp")
                self.value["files"] = resizeImage(images)
                return self.value["files"]
            else:
                return None
