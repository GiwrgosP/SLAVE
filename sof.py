
from docx import Document
import tkinter as tk
import os
import sqlite3
import formsWindow
import fileSelectionWindow

#window object
class window(tk.Tk):
    def __del__(self):
        print("Ending")
        self.con.close()

    def __init__(self):
        #find the path of the current file
        self.path = os.path.dirname(os.path.abspath(__file__))
        #make the fileSelected paremeter equal to None
        #using this paremeter to check the state of the window that will be shown
        self.fileSelected = None
        #create the database connection paremeters
        self.c,self.con = self.conn()
        #create a window object
        self.window = tk.Tk()
        #name it
        self.window.title("Sophi's Loyal Assistant Veterinarian Edition")
        #size it
        self.window.geometry("1408x512")
        #call the checkState function to fill the window
        self.checkState()

    def collectOneValue(self,data):
        temp = list()
        for i in data:
            temp.append(i[0])
        return temp

#database connection paremeters
    def conn(self):
        str = self.path +"\\dataBase.db"
        try:
            con = sqlite3.connect(str)
            c = con.cursor()
            return c,con
        except:
            print("Error While Connectiong To DataBase", str)

#get all file that are on the data base files table [fieldId,testId,langId,petId,filePath]
    def getFile(self):
        self.c.execute("SELECT * FROM files")
        rows = self.c.fetchall()
        return rows

#get widgets for the form selected form[fileId,widgetId]
    def getForm(self,fileId):
        self.c.execute("SELECT widgetId FROM form WHERE fileId = ?", (fileId,))
        rows = self.c.fetchall()
        return self.collectOneValue(rows)

    def getWidget(self,widgetId):
        self.c.execute("SELECT objectId,name,nameVal,sort FROM widget WHERE widgetId = ?", (widgetId,))
        rows = self.c.fetchall()
        return rows[0]

    def getWidgetMenuId(self,widgetId):
        self.c.execute("SELECT menuId FROM widgetMenus WHERE widgetId = ?", (widgetId,))
        rows = self.c.fetchall()
        return self.collectOneValue(rows)

    def getValues(self,widgetMenuId):
        self.c.execute("SELECT value FROM menuValues WHERE menuId = ?", (widgetMenuId,))
        rows = self.c.fetchall()
        return self.collectOneValue(rows)

    def getEksetasi(self):
        self.c.execute("SELECT * FROM Eksetasi")
        rows = self.c.fetchall()
        return rows

    def getThema(self):
        self.c.execute("SELECT text FROM thema")
        rows = self.c.fetchall()
        return self.collectOneValue(rows)

    def getCategory(self,themaId):
        self.c.execute("SELECT text FROM categoryThema WHERE id_thema = ?", (themaId,))
        rows = self.c.fetchall()
        return self.collectOneValue(rows)

    def getTitles(self,categoryId):
        self.c.execute("SELECT text FROM titlesCategories WHERE id_thema = ?", (categoryId,))
        rows = self.c.fetchall()
        return self.collectOneValue(rows)

    def getPetWeightIndex(self,petId):
        self.c.execute("SELECT average,tooMuch FROM petWeightIndex WHERE petId = ?", (petId,))
        rows = self.c.fetchall()
        return rows[0]

    def getPetAgeIndex(self,petId):
        self.c.execute("SELECT adult,elder FROM petAgeIndex WHERE petId = ?", (petId,))
        rows = self.c.fetchall()
        return rows[0]

    def createValue(self,value,field):
        self.c.execute("INSERT INTO menuValues (menuId,value) VALUES(?,?)", (field,value,))
        self.con.commit()

    #check if any selection objects that have been made and delete them
    #then create a new selection object based on fileSelected
    def checkState(self):
        try:
            del self.selection
        except:
            pass
        if self.fileSelected == None:
            self.selection = fileSelectionWindow.fileSelectionWindow(self)
        else:
            self.selection = formsWindow.formWindow(self)

#main, create and run the tkinter object
def main():
    root = window()
    root.window.mainloop()

#call the main function
main()
