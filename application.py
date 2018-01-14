import pyLight
from gui import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class PyLightApp(Ui_MainWindow):
    def __init__(self, window):
        #Ui_MainWindow.__init__(self)
        self.setupUi(window)

        self.connect_slots()

    def connect_slots(self):
        self.applyButton.clicked.connect(self.doApply)

    def doApply(self):
        print("Apply Pressed")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    window = PyLightApp(main_window)
    main_window.show()
    sys.exit(app.exec_())