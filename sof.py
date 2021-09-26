from docx import Document
import tkinter as tk
import os
import sqlite3
import formWindow
import fileSelectionWindow


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

    def getFile(self):
        self.c.execute("SELECT * FROM files")
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

    def checkState(self):
        try:
            del self.selection
        except:
            pass
        if self.fileSelected == None:
            self.selection = fileSelectionWindow.fileSelectionWindow(self)
        else:
            self.selection = formWindow.formWindow(self)

def main():
    root = window()
    root.window.mainloop()


main()
