from math import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow
import sys

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.calculatebutton.clicked.connect(self.calculate)
        self.deletebutton.clicked.connect(self.reset)

    def calculate(self):
        self.ConsoleWindowText.setText("-")
        self.ConsoleWindowText.setStyleSheet("color: rgb(255, 255, 255);")
        realPower = is_input_float(self, self.RealPowerText.text())
        reactivePower = is_input_float(self, self.ReactivePowerText.text())
        apparentPower = is_input_float(self, self.ApparentPowerText.text())
        voltage = is_input_float(self, self.VoltageText.text())
        powerFactor = is_input_float(self, self.PowerFactorText.text())

        if (realPower is not None) and (powerFactor is not None):
            reactivePower = realPower * tan(acos(powerFactor))
            apparentPower = realPower / cos(acos(powerFactor))
        elif (reactivePower is not None) and (powerFactor is not None):
            if powerFactor == 1.0:
                self.ConsoleWindowText.setText("No MVAr at unity PF")
                self.ConsoleWindowText.setStyleSheet("color: rgb(255, 0, 0);")
            else:
                realPower = reactivePower / tan(acos(powerFactor))
                apparentPower = reactivePower / sin(acos(powerFactor))
        elif (apparentPower is not None) and (powerFactor is not None):
            realPower = apparentPower * cos(acos(powerFactor))
            reactivePower = apparentPower * sin(acos(powerFactor))
        elif (apparentPower is not None) and (realPower is not None):
            powerFactor = realPower / apparentPower
            reactivePower = apparentPower * (sqrt( 1 - (powerFactor ** 2)))
        elif (apparentPower is not None) and (reactivePower is not None):
            powerFactorAngle = asin(reactivePower / apparentPower)
            powerFactor = cos(powerFactorAngle)
            realPower = apparentPower * powerFactor
        elif (realPower is not None) and (reactivePower is not None):
            powerFactorAngle = atan(reactivePower / realPower)
            powerFactor = cos(powerFactorAngle)
            apparentPower = realPower / powerFactor
        else:
            self.ConsoleWindowText.setText("Invalid, please enter 2 power entries or 1 power and PF")
            self.ConsoleWindowText.setStyleSheet("color: rgb(255, 0, 0);")
            return

        if voltage is not None:
            realcurrent = round((realPower / (sqrt(3) * voltage)), 3)
            reactivecurrent = round((reactivePower / (sqrt(3) * voltage)), 3)
            self.CurrentText.setText(str(realcurrent) + " A")
            self.ReactiveCurrentText.setText(str(reactivecurrent) + " A")
        else:
            voltage = 0

        self.RealPowerText.setText(str(round(realPower,3)))
        self.ReactivePowerText.setText(str(round(reactivePower,3)))
        self.ApparentPowerText.setText(str(round(apparentPower,3)))
        self.PowerFactorText.setText(str(round(powerFactor,3)))
        self.VoltageText.setText(str(round(voltage,3)))


    def reset(self):
        self.RealPowerText.setText("")
        self.ReactivePowerText.setText("")
        self.ApparentPowerText.setText("")
        self.VoltageText.setText("")
        self.PowerFactorText.setText("")
        self.CurrentText.setText("-")
        self.ReactiveCurrentText.setText("-")
        self.ConsoleWindowText.setText("-")
        self.ConsoleWindowText.setStyleSheet("color: rgb(255, 255, 255);")


def is_input_float(unit, input):
    if input=="":
        return
    else:
        try:
            float(input)
            return float(input)
        except ValueError:
            unit.ConsoleWindowText.setText("Inputs aren't numbers.")
            unit.ConsoleWindowText.setStyleSheet("color: rgb(255, 0, 0);")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

