import tkinter as tk
import db as db
from docxtpl import DocxTemplate

class fileSelectionWindow(tk.Tk):
    def __init__(self,path):
        self.window = tk.Tk()
        self.window.title("Sophi's Loyal Assistant Vet Edition")
        self.window.geometry("1024x512")
        self.entryEntities = db.getFirstFields(path)
        self.leftFrameButtons = {}
        self.rightFrameButtons = {}
        self.leftFrame = tk.Frame(self.window)
        self.rightFrame = tk.Frame(self.window)

        self.leftFrameButtons["labelGreek"] = tk.Label(self.leftFrame, text = "greek")
        self.rightFrameButtons["labelEnglish"] = tk.Label(self.rightFrame, text = "english")


        for ent in self.entryEntities:

            if ent[3] == "greek":
                self.leftFrameButtons[ent[0]] = tk.Button(self.leftFrame, text = ent[1], command = lambda fileName = ent[2], file = ent[0]: self.openTemplate(path,fileName,file))
            elif ent[3] == "english":
                self.rightFrameButtons[ent[0]] = tk.Button(self.rightFrame, text = ent[1], command = lambda fileName = ent[2], file = ent[0]: self.openTemplate(path,fileName,file))

        self.gridFrame(self.leftFrameButtons)
        self.gridFrame(self.rightFrameButtons)
        self.leftFrame.pack(side = tk.LEFT)
        self.rightFrame.pack(side = tk.RIGHT)
        self.window.mainloop()

    def gridFrame(self,frameButtons):
        row = 0
        column = 0
        for ent in frameButtons:
            frameButtons[ent].grid(column = column, row = row)
            column += 1
            if column == 5:
                column = 0
                row += 1



    def openTemplate(self,path,fileName,file):
        if fileName != None:
            str = path + "\\" +fileName
            try:
                doc = DocxTemplate(str)
                self.file = file
                self.window.destroy()

            except:
                print("error with file path name")
        else:
            print("file name is none in datebase")
