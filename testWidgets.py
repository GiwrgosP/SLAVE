
class ageSpinBoxEnt(tk.Tk):
    def __init__(self, master, ent):
        self.master = master
        self.text = ent[1]
        self.name = ent[2]
        self.value = tk.DoubleVar()
        self.mainWidgetFrame = tk.Frame(self.master.inputFrame)
        self.widgets = list()
        self.widgetsInput = list()

        spinBoxLabel = tk.Label(self.mainWidgetFrame, text = self.text)
        self.widgets.append(spinBoxLabel)

        spinBoxWidget = tk.Spinbox(self.mainWidgetFrame, from_ = 0, to = 1000, increment=0.1, format= "%.1f",command = lambda: self.giveValues())
        self.widgets.append(spinBoxWidget)
        self.widgetsInput.append(spinBoxWidget)

        radioButton1 = tk.Radiobutton(root, text="Μηνών", value=1, command=sel)
        self.widgets.append(radioButton1)
        self.widgetsInput.append(radioButton1)

        radioButton2 = tk.Radiobutton(root, text="Χρονών", value=2, command=sel)
        radioButton2.select()
        self.widgets.append(radioButton2)
        self.widgetsInput.append(radioButton2)

        self.gridWidgets()
        self.mainWidgetFrame.grid(column = 0, row = ent[5]-1)


    def checkSelf(self):
        pass

    def giveValues(self):
        spinBoxWeight = float(self.master.entries["weight"].widgetsInput[0].get())
        spinBoxAge = float(self.master.entries["age"].widgetsInput[0].get())

        if spinBoxWeight != 0.00 and spinBoxAge != 0.00:

            if spinBoxWeight<= 15.00:
                weight = "μικρόσωμο"
            elif spinBoxWeight <= 55.00:
                weight = "μεγαλόσωμο"
            else:
                weight = "γιαγαντόσωμο"

            if spinBoxAge<= 4.00:
                age = "νεαρό"
            elif spinBoxAge <= 8.00:
                age = "ενήλικο"
            else:
                age = "υπερήλικο"

            self.master.entries["cardiologicalAnalysis"].values = (("Καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο με υποψία καρδιακής νόσου.",),\
                                                ("Προεγχειρητικός καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",),\
                                                ("Προληπτικός καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",),\
                                                ("Προεγχειρητικός και προληπτικός  καρδιολογικός έλεγχος σε "+weight+" "+age+" σκύλο.",))
            self.master.entries["cardiologicalAnalysis"].applyValues()
        else:
            pass

    def gridWidgets(self):
        column = 0
        for ent in self.widgets:
            ent.grid(column = column, row = 0)
            column += 1

    def getWidgetValues(self):
        age = self.widgetInput[0].get()
        timeAproximation = self.widgetInput[2].get()

        flagPlural = True
        if age == 1:
            flagPlural = False

        if timeAproximation == 2:
            textTimeAproximation = " χρονών"
            if flagPlural == False:
                textTimeAproximation = " έτους"
        else:
            textTimeAproximation = " μηνών"
            if flagPlural == False:
                textTimeAproximation = " μηνώς"

        return age + timeAproximation
