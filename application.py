import pyLight
from gui import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread

class PyLightApp(Ui_MainWindow):
    def __init__(self, window):
        # Ui_MainWindow.__init__(self)
        self.setupUi(window)
        self.controller = None

        self.populateComboBoxes()
        self.connect_slots()

    def connect_slots(self):
        self.applyButton.clicked.connect(self.doApply)

    def populateComboBoxes(self):
        for key in pyLight.CONTROL_MODES:
            self.controlModeComboBox.addItem(key)

    def doApply(self):
        control = self.controlModeComboBox.currentText()
        if self.controller:
            self.worker.stop()

        self.controller = pyLight.CONTROL_MODES[control]

        self.worker = workerThread(self.controller)
        self.worker.start()


class workerThread(QThread):
    def __init__(self, worker):
        QThread.__init__(self)
        self.worker = worker

    def __del__(self):
        self.wait()

    def run(self):
        self.controller = self.worker('COM4')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    window = PyLightApp(main_window)
    main_window.show()
    sys.exit(app.exec_())