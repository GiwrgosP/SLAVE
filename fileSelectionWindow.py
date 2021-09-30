import tkinter as tk
from docxtpl import DocxTemplate
from docx import Document
import os
from tkinter import filedialog,messagebox


#a dictionary to divide the files data by lang and pet
def divideOptions(optionsList):
    teams = { "greek" : { "dog" : list(), "cat" : list()}, "english" : { "dog" : list(), "cat" : list()}}

    for option in optionsList:
        teams[option[2]][option[3]].append((option[0],option[1],option[2],option[3],option[4]))

    return teams

class fileSelectionWindow(tk.Tk):
    def __del__(self):
        print("Ending fileSelectionWindow")


    def __init__(self,master):
        #reference to window class as master
        self.master = master
        #call getFile() from class window to get a list of all files for display
        self.files = self.master.getFile()
        #create a frame inside the window class
        self.mainFrame = tk.Frame(self.master.window, background = "MediumPurple4")
        #call a function to divide the files list into subcategories
        teams = divideOptions(self.files)
        #make a grid of widegts and place them into each category and subcategory frame
        for lang in teams:
            frame = tk.Frame(self.mainFrame,background = "steel blue")
            label = tk.Label(frame, text = lang)
            label.pack()

            for pet in teams[lang]:
                frame2 = tk.Frame(frame,background = "grey60")
                label2 = tk.Label(frame2, text = pet)
                label2.grid(column = 0, row = 0)
                row2 = column2 = 1
                for i in teams[lang][pet]:
                    if column2 == 15:
                        row2 += 1
                        column2 = 0
                    button = tk.Button(frame2,text = i[1],background = "salmon2", command = lambda x = i :self.openTemplate(x))
                    if i[4] == None:
                        button.configure(state = "disabled")
                    button.grid(column = column2,row = row2, padx = 5, pady = 5, sticky = "we")
                    column2 += 1

                frame2.pack()

            frame.pack()

        self.mainFrame.pack(fill='both', expand = True)

    #for every button available try to open its word document, if it succeed
    #make the window class selection value equal to the doc info
    #and destroy this fileSelectionWindow object
    def openTemplate(self,ent):
        str = self.master.path + "\\Protipa\\" + ent[4]
        try:
            doc = DocxTemplate(str)
        except:
            messagebox.showerror(title = "Slave could not complete your request", message = "Slave encounterred an error while trying to open the file asked or create the form")
        else:
            self.master.fileSelected = ent
            self.mainFrame.destroy()
            self.master.checkState()
