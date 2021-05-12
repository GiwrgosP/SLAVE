import tkinter as tk
from tkinter import filedialog

class forms(tk.Tk):

    class entry(tk.Tk):

        def __init__(self,master,name) :
            self.master = master
            self.frame = tk.Frame(self.master.inputFrame)
            self.label = tk.Label(self.frame, text = name)

            self.entry = tk.Entry(self.frame)

            self.label.pack(side = "left")
            self.entry.pack(side = "left")
            self.frame.pack(fill = "x", expand = "True")

    class menuEnt(tk.Tk):

        def __init__(self, master, name, widgetId) :
            self.master = master
            self.frame = tk.Frame(self.master.inputFrame)
            self.label = tk.Label(self.frame, text = name)
            self.entry = tk.Entry(self.frame)
            self.menu = tk.Menubutton(self.frame)
            self.menu.menu = tk.Menu(self.menu)
            self.menu["menu"] = self.menu.menu
            print("+++++++++++++++++++++++++")
            print(widgetId)
            a = self.master.master.getWidgetMenus(widgetId)
            print(a[0][0])
            menuValues = self.master.master.getValues(a[0][0])




            for value in menuValues:
                #Το κουμπί θέλει διόρθωση!
                self.menu.menu.add_radiobutton(label = value, value = value)
                print(value)
            self.label.pack(side = "left")
            self.entry.pack(side = "left")
            self.menu.pack(side = "left")
            self.frame.pack(fill = "x", expand = "True")


    def createWidgets(self) :
        self.widgetList = list()
        self.widgetValues = list()
        for widget in self.form:
            temp = self.master.getWidget(widget[0])
            if temp[0] == "entry":
                self.widgetList.append(self.entry(self,temp[2]))
            elif temp[0] == "menuEnt":
                self.widgetList.append(self.menuEnt(self,temp[2],widget[0]))
            else:
                pass



    def createScrollbar(self):
        self.canvas.update_idletasks()
        self.scrollBar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.scrollBar.grid(row = 0, column = 3, sticky = "ns")
        self.updateScrollBar()
        self.canvas.configure(scrollregion=self.canvas.bbox('both'),yscrollcommand=self.scrollBar.set)
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def updateScrollBar(self):
        self.canvas.configure(scrollregion=self.canvas.bbox('both'),yscrollcommand=self.scrollBar.set)

    def onMouseWheel(self, event):
        scrollDir = int(event.delta/120)
        self.canvas.yview('scroll',-1*scrollDir, "units")
        self.updateScrollBar()

    def __init__(self,master,widgets):
        self.master = master
        self.form = widgets

        self.canvas = tk.Canvas (self.master.window)
        self.inputFrame = tk.Frame(self.canvas, background = "salmon2", width = "500", height = "500")
        self.canvas.create_window(0, 0,anchor = "nw", window=self.inputFrame)
        self.createWidgets()
        self.canvas.grid_columnconfigure(0, weight=3)
        self.createScrollbar()
        self.inputFrame.grid(column = 0, row = 0)
        self.canvas.pack(expand = "True", fill = "both")
