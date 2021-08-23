from docx import Document
import tkinter as tk
import os
import sqlite3
import formWindow
import fileSelection

class window(tk.Tk):
    def __del__(self):
        print("Ending")
        self.con.close()


    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.fileSelected = None
        self.c,self.con = self.conn()
        self.window = tk.Tk()
        self.window.title("Sophi's Loyal Assistant Veterinarian Edition")
        self.window.geometry("1024x512")
        self.checkState()

    def conn(self):
        str = self.path +"\\dataBase.db"
        try:
            con = sqlite3.connect(str)
            c = con.cursor()
            return c,con
        except:
            print("Error While Connectiong To DataBase", str)

    def getFile(self,text,value):
        self.c.execute("SELECT * FROM files"+text,value)
        rows = self.c.fetchall()
        return rows

    def getPets(self):
        self.c.execute("SELECT * FROM pets")
        rows = self.c.fetchall()
        return rows

    def getLangs(self):
        self.c.execute("SELECT * FROM language")
        rows = self.c.fetchall()
        return rows

    def getForm(self,widgetId):
        self.c.execute("SELECT widgetId FROM form WHERE fileId = ?", (widgetId,))
        rows = self.c.fetchall()
        return rows

    def getWidget(self,widgetId):
        self.c.execute("SELECT objectId,name,nameVal,sort FROM widget WHERE widgetId = ?", (widgetId,))
        rows = self.c.fetchall()
        return rows[0]

    def getWidgetMenus(self,widgetId):
        self.c.execute("SELECT menuId FROM widgetMenus WHERE widgetId = ?", (widgetId,))
        rows = self.c.fetchall()
        return rows

    def getValues(self,widgetMenuId):
        self.c.execute("SELECT value FROM menuValues WHERE menuId = ?", (widgetMenuId,))
        rows = self.c.fetchall()
        temp = list()
        for row in rows:
            temp.append(row[0])
        return temp

    def getEksetasi(self):
        self.c.execute("SELECT * FROM Eksetasi")
        rows = self.c.fetchall()
        return rows

    def getPetWeightIndex(self,petId):
        self.c.execute("SELECT small,average,tooMuch FROM petWeightIndex WHERE petId = ?", (petId,))
        rows = self.c.fetchall()
        return rows[0]

    def getPetAgeIndex(self,petId):
        self.c.execute("SELECT young,adult,elder FROM petAgeIndex WHERE petId = ?", (petId,))
        rows = self.c.fetchall()
        return rows[0]

    def createValue(self,value,field):
        self.c.execute("INSERT INTO menuValues (menuId,value) VALUES(?,?)", (field,value,))
        self.con.commit()

    def checkState(self):
        print(self.fileSelected)
        try:
            print("delete selection")
            del self.selection
        except:
            pass
        if self.fileSelected == None:
            self.selection = fileSelection.fileSelectionWindow(self)
        elif self.fileSelected == "form":
            self.selection = fileForms.form(self)
        else:
            pass

def main():
    root = window()
    root.window.mainloop()


main()
