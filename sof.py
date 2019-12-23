from docx import Document

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
