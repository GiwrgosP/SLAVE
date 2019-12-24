from docx import Document
import tkinter as tk
import os

import mainWindow
import fileSelectionWindow
import db as db

class window(tk.Tk):
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.fileSelected = None
        self.createWindow()

    def createWindow(self):
        self.window = tk.Tk()
        self.window.title("Sophi's Loyal Assistant Veterinarian Edition")
        self.window.geometry("1024x512")

        self.checkState()

    def checkState(self):
        if self.fileSelected == None:
            selection = fileSelectionWindow.fileSelectionWindow(self)
        else:
            selection = mainWindow.mainWindow(self)

def main():
    root = window()


main()
