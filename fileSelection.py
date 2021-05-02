import tkinter as tk

class fileSelectionWindow(tk.Tk):
    def checkChoice(self,value,var):
        var.set(value)
        if self.petVar.get() != "+++" and self.langVar.get() != "+++":
            temp = " WHERE langId = ? AND petId = ?"
            print(temp)
            values = self.master.getFile(temp,(self.langVar.get(),self.petVar.get()))
            self.frame3.fillFrame(values)


    class filterFrame():
        def __init__(self,master,name,row,choices,textVar):
            self.master = master
            self.frame = tk.Frame(self.master.mainFrame,background = "salmon2")
            self.label = tk.Label(self.frame, text = name)
            self.label.grid(row = 1, column = 2)
            counter = 1
            for i in choices:
                temp = tk.Button(self.frame, text = i[0], command = lambda x=i[0],y=textVar : self.master.checkChoice(x,y), padx = "5", pady = "5")
                temp.grid(row = 2, column = counter)
                counter = 3
            self.frame.grid(row = row, column = 1,  padx = "5", pady = "55")

    class choiceFrame():
        def fileSelected(self,x):
            self.master.master.fileSelected = x
            self.master.master.checkState()
            
        def __init__(self,master,name):
            self.master = master
            self.frame = tk.Frame(self.master.mainFrame)
            self.canvas = tk.Canvas(self.frame, confine = True)
            self.inputFrame = tk.Frame(self.canvas, background = "salmon2", width = "100", height = "100")
            self.canvas.create_window(0, 0,anchor = "nw", window=self.inputFrame)
            self.createScrollbar()

            self.frameButtons = list()
            self.canvas.grid(row = 1, column = 2)
            self.frame.grid(row = 1, column = 2)
            
        def fillFrame(self,choices):
            print(len(self.frameButtons))
            if len(self.frameButtons) > 0:
                for but in self.frameButtons:
                    but.destroy()
                self.inputFrame.destroy()
                self.frameButtons.clear()
                self.inputFrame = tk.Frame(self.canvas, background = "salmon2")
            counterColumn = 1
            counterRow = 1
            for i in choices:
                self.frameButtons.append(tk.Button(self.inputFrame,text = i[1], command = lambda x = i[4] : self.fileSelected (x)))
                self.frameButtons[-1].grid(row = counterRow, column = counterColumn, padx = "5", pady = "5")
                counterColumn += 1
                if counterColumn == 6: 
                    counterRow += 1
                    counterColumn = 1
                 
            self.canvas.create_window(0, 0, anchor = "nw", window=self.inputFrame)


        def createScrollbar(self):
            self.canvas.update_idletasks()
            self.scrollBar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
            self.scrollBar.pack(fill='y', side='right')

            self.updateScrollBar()


            self.canvas.configure(scrollregion=self.canvas.bbox('both'),yscrollcommand=self.scrollBar.set)

            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

        def updateScrollBar(self):
            self.canvas.configure(scrollregion=self.canvas.bbox('both'),yscrollcommand=self.scrollBar.set)

        def onMouseWheel(self, event):
            scrollDir = int(event.delta/120)
            self.canvas.yview('scroll',-1*scrollDir, "units")
            self.updateScrollBar()


    def __del__(self):
        print("Ending fileSelectionWindow")

    def __init__(self,master):
        self.master = master
        self.petVar = tk.StringVar(value = "+++")
        self.langVar = tk.StringVar(value = "+++")
        self.mainFrame =  tk.Frame(self.master.window, background = "steel blue")
        frame1 = self.filterFrame(self,"lang",1,self.master.getLangs(),self.langVar)
        frame2 = self.filterFrame(self,"pet",2,self.master.getPets(),self.petVar)
        self.frame3 = self.choiceFrame(self,"lang")
        self.mainFrame.pack(fill='both', expand = True)
