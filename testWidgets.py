class medicMenuEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.field = ent[0]
        self.text = ent[1]
        self.name = ent[2]
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.frames = list()
        self.menuValue = list()
        self.widgets = list()
        self.widgetsInput = list()

        self.createWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)

    def createWidgets(self):
        widgetFrame = tk.Frame(self.mainWidgetFrame)
        self.frames.append(widgetFrame)

        addButton = tk.Button(widgetFrame, text = "+", command = self.createWidgets)
        destroyButton = tk.Button(widgetFrame, text = "-", command = lambda x = widgetFrame: self.destroyButtonAction(x))

        values = db.getFieldValues(self.field,self.master.master.path)

        menuWidget = tk.Menubutton(widgetFrame, text = self.text)
        menuWidget.menu = tk.Menu(menuWidget)
        menuWidget["menu"] = menuWidget.menu

        temp = len(self.menuValue)
        self.menuValue.append(tk.StringVar())

        for val in values:
            menuWidget.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[temp])

        menuEntry = tk.Entry(widgetFrame, text = self.menuValue[temp])

        spinBoxWidget = tk.Spinbox(widgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f")

        values3 = db.getFieldValues(25,self.master.master.path)

        menuWidget3 = tk.Menubutton(widgetFrame, text = "Μονάδα μέτρησης")
        menuWidget3.menu = tk.Menu(menuWidget3)
        menuWidget3["menu"] = menuWidget3.menu

        temp = len(self.menuValue)
        self.menuValue.append(tk.StringVar())

        for val in values3:
            menuWidget3.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[temp])

        menuEntry3 = tk.Entry(widgetFrame, text = self.menuValue[temp])

        values2 = db.getFieldValues(26,self.master.master.path)

        menuWidget2 = tk.Menubutton(widgetFrame, text = "Δοσολογία")
        menuWidget2.menu = tk.Menu(menuWidget2)
        menuWidget2["menu"] = menuWidget2.menu

        temp = len(self.menuValue)
        self.menuValue.append(tk.StringVar())

        for val in values2:
            menuWidget2.menu.add_radiobutton(label = val[0], value = val[0],variable = self.menuValue[temp])

        menuEntry2 = tk.Entry(widgetFrame, text = self.menuValue[temp])

        tempListWidgets = list()
        tempListWidgetsInput = list()

        tempListWidgets.append(addButton)
        tempListWidgets.append(destroyButton)

        tempListWidgets.append(menuWidget)

        tempListWidgets.append(menuEntry)
        tempListWidgetsInput.append(menuEntry)

        tempListWidgets.append(spinBoxWidget)
        tempListWidgetsInput.append(spinBoxWidget)

        tempListWidgets.append(menuWidget3)

        tempListWidgets.append(menuEntry3)
        tempListWidgetsInput.append(menuEntry3)

        tempListWidgets.append(menuWidget2)

        tempListWidgets.append(menuEntry2)
        tempListWidgetsInput.append(menuEntry2)

        self.widgets.append(tempListWidgets)
        self.widgetsInput.append(tempListWidgetsInput)

        self.gridWidgets()
        widgetFrame.grid()

    def gridWidgets(self):
        for frame in self.widgets:
            column = 0
            for ent in frame:
                ent.grid(column = column, row = 0)
                column += 1

    def destroyButtonAction(self,frameForDel):
        if len(self.frames) == 1:
            print("no more frames available for delete")
        else:
            counter = 0
            for frame in self.frames:
                if frame == frameForDel:
                    break
                else:
                    counter += 1

            self.frames[counter].destroy()
            del self.frames[counter]
            del self.menuValue[counter]
            del self.widgets[counter]
            del self.widgetsInput[counter]

    def getWidgetValues(self):
        values = list()
        for ent in self.widgetsInput:
            groupValue = list()
            groupValue.append(ent[0].get())
            groupValue.append(" (" + ent[1].get() + " " + ent[2].get()+ " " + ent[3].get() + "), ")
            values.append(groupValue)

        values[-1][1] = values[-1][1][:-2]
        return values
