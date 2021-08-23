import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from docxtpl import DocxTemplate
from tkinter import filedialog
import fileForms

class form(tk.Tk):
    def __init__(self,master):
        self.master = master
        self.mainFrame = tk.Frame(self.master.window,background = "alice blue")
        self.mainFrame.pack()
