import tkinter as tk
import db as db
from docxtpl import DocxTemplate
from docx import Document
import os

def divideOptions(optionsList):
    teams = { "greek" : { "dog" : list(), "cat" : list()}, "english" : { "dog" : list(), "cat" : list()}}

    for option in optionsList:
        teams[option[2]][option[3]].append((option[0],option[1],option[4]))

    return teams



class fileSelectionWindow(tk.Tk):
    def __init__(self,master):
        self.master = master
        self.files = db.getFile(self.master.path)
        self.mainFrame = tk.Frame(self.master.window, background = "grey40")

        teams = divideOptions(self.files)

        for lang in teams:
            frame = tk.Frame(self.mainFrame,background = "grey60")
            label = tk.Label(frame, text = lang)
            label.pack()

            for pet in teams[lang]:
                frame2 = tk.Frame(frame,background = "gray80")
                label2 = tk.Label(frame2, text = pet)
                label2.grid(column = 0, row = 0)
                row2 = column2 = 1
                for i in teams[lang][pet]:
                    if column2 == 15:
                        row2 += 1
                        column2 = 0
                    button = tk.Button(frame2,text = i[1], command = lambda x = i :self.openTemplate(x))
                    if i[2] == None:
                        button.configure(state = "disabled")
                    button.grid(column = column2,row = row2, padx = 5, pady = 5, sticky = "we")
                    column2 += 1

                frame2.pack()

            frame.pack()

        self.mainFrame.pack(fill='both')
        self.master.window.mainloop()

    def openTemplate(self,ent):
        print(ent)
        str = self.master.path + "\\Protipa\\" + ent[2]
        #try:
        doc = DocxTemplate(str)
        self.master.fileSelected = ent
        self.master.window.destroy()
        self.master.createWindow()
        #except:
        #print("error opening file")
