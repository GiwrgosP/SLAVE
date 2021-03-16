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
        def __init__(self,master,name,choices,textVar):
            self.master = master
            self.frame = tk.Frame(self.master.mainFrame,background = "salmon2")
            for i in choices:
                temp = tk.Button(self.frame, text = i[0], command = lambda x=i[0],y=textVar : self.master.checkChoice(x,y))
                temp.pack()
            self.frame.pack(side = "left", fill='y', expand = True)

    class choiceFrame():
        def __init__(self,master,name):
            self.master = master
            self.canvas = tk.Canvas(self.master.mainFrame, confine = True)
            self.inputFrame = tk.Frame(self.canvas, background = "salmon2")
            self.canvas.create_window(0, 0,anchor = "nw", window=self.inputFrame)
            self.createScrollbar()

            self.frameButtons = list()
            self.canvas.pack(fill = 'y')

        def fillFrame(self,choices):
            print(len(self.frameButtons))
            if len(self.frameButtons) > 0:
                for but in self.frameButtons:
                    but.destroy()
                self.inputFrame.destroy()
                self.frameButtons.clear()
                self.inputFrame = tk.Frame(self.canvas, background = "salmon2")
            for i in choices:
                self.frameButtons.append(tk.Button(self.inputFrame,text = i[1]))
                self.frameButtons[-1].pack()

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
        frame1 = self.filterFrame(self,"lang",self.master.getPets(),self.petVar)
        frame2 = self.filterFrame(self,"lang",self.master.getLangs(),self.langVar)
        self.frame3 = self.choiceFrame(self,"lang")
        self.mainFrame.pack(fill='both', expand = True)
