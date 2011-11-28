# [h] hello vanilla world

from vanilla import *

class SimpleAppWindow(object):

    def __init__(self):
        self.w = Window((250, 600), "VanillaTest")
        self.w.text = TextBox((10, 10, -10, 70), "This is a simple window.")
        self.w.slider = Slider((10, 40, -10, 23), tickMarkCount=10, callback=self.sliderCallback)
        self.w.editText = EditText((10, 80, -10, 22), callback=self.editTextCallback)
        self.w.discreteIndicator = LevelIndicator((10, 120, -10, 18), callback=self.levelIndicatorCallback)
        self.w.continuousIndicator = LevelIndicator((10, 160, -10, 18), style="continuous", callback=self.levelIndicatorCallback, warningValue=75.00, criticalValue=90.00, minValue=0, maxValue=100.00, value=30.00)
        self.w.radioGroup = RadioGroup((10, 200, -10, 40), ["Option 1", "Option 2"], callback=self.radioGroupCallback)
        self.w.popUpButton = PopUpButton((10, 320, -10, 20), ["A", "B", "C"], callback=self.popUpButtonCallback)
        self.w.box = Box((10, 250, -10, 50))
        self.w.box.text = TextBox((5, 5, -10, -10), "This is a box")
        self.w.comboBox = ComboBox((10, 360, -10, 21), ["AA", "BB", "CC", "DD"], callback=self.comboBoxCallback)
        self.w.checkBox = CheckBox((10, 390, -10, 20), "A CheckBox", callback=self.checkBoxCallback, value=True)
        self.w.button = Button((10, -40, -10, 20), "Press me", callback=self.buttonCallback)
        self.d = Drawer((100, 150), self.w)
        self.d.textBox = TextBox((10, 10, -10, -10), "This is a drawer.")
        self.w.open()
        self.d.open()

    def buttonCallback(self, sender):
        print "You pressed the button!"
        self.d.toggle()

    def sliderCallback(self, sender):
        _value = sender.get()
        print "slider edit!", _value
        self.w.continuousIndicator.set(_value)

    def editTextCallback(self, sender):
        print "text entry!", sender.get()

    def levelIndicatorCallback(self, sender):
        print "level indicator edit!", sender.get()

    def toggleDrawer(self, sender):
        self.d.toggle()

    def radioGroupCallback(self, sender):
        print "radio group edit!", sender.get()

    def popUpButtonCallback(self, sender):
        print "pop up button selection!", sender.get()

    def comboBoxCallback(self, sender):
        print "combo box entry!", sender.get()

    def checkBoxCallback(self, sender):
        print "check box state change!", sender.get()

SimpleAppWindow()

