import tkinter as tk
import db as db
from docxtpl import DocxTemplate
from docx import Document
import os

class fileSelectionWindow(tk.Tk):
    def __init__(self,master):
        self.master = master

        self.entryEntities = db.getFirstFields(self.master.path)

        self.leftFrameButtons = {}
        self.rightFrameButtons = {}

        self.leftFrame = tk.Frame(self.master.window)
        self.rightFrame = tk.Frame(self.master.window)

        self.leftFrameButtons["labelGreek"] = tk.Label(self.leftFrame, text = "greek")
        self.rightFrameButtons["labelEnglish"] = tk.Label(self.rightFrame, text = "english")


        for ent in self.entryEntities:

            if ent[3] == "greek":
                self.leftFrameButtons[ent[0]] = tk.Button(self.leftFrame, text = ent[1], command = lambda ent = ent: self.openTemplate(ent))
            elif ent[3] == "english":
                self.rightFrameButtons[ent[0]] = tk.Button(self.rightFrame, text = ent[1], command = lambda ent = ent: self.openTemplate(ent))

        self.gridFrame(self.leftFrameButtons)
        self.gridFrame(self.rightFrameButtons)
        self.leftFrame.pack(side = tk.LEFT)
        self.rightFrame.pack(side = tk.RIGHT)
        self.master.window.mainloop()

    def gridFrame(self,frameButtons):
        row = 0
        column = 0
        for ent in frameButtons:
            frameButtons[ent].grid(column = column, row = row)
            column += 1
            if column == 5:
                column = 0
                row += 1

    def openTemplate(self,ent):
        if ent[2] != None:
            str = self.master.path + "\\" + ent[2]
            print(ent[2])
            try:
                doc = DocxTemplate(str)
                self.master.fileSelected = ent
                self.master.window.destroy()
                self.master.createWindow()

            except:
                print("error with file path name")
        else:
            print("file name is none in datebase")
