import tkinter as tk

from docx import Document
from docxtpl import DocxTemplate

import os

import mainWindow
import fileSelectionWindow
import db as db


path = os.path.dirname(os.path.abspath(__file__))


def main():
    selection = fileSelectionWindow.fileSelectionWindow(path)
    print(selection.file)
    window = mainWindow.mainWindow(path)



main()
