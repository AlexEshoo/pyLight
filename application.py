import pyLight
from gui import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread
import threading
import time

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
        print("Applying")
        control = self.controlModeComboBox.currentText()
        if self.controller:
            print("Controller exists...")
            self.controller.disconnect()
            #self.worker.stop()
            #self.worker.join()

        self.controller = pyLight.CONTROL_MODES[control]("COM4")
        print("made object")
        self.controller.begin_control()

        #self.worker = WorkerThread(self.controller)
        #self.worker.start()
        print("end")


class WorkerThread(threading.Thread):
    """"
    Only works with Screenshot controller at the moment. Need to implement
    better class structure to approach this from a polymorphic angle.
    """
    def __init__(self, worker):
        super().__init__()
        self.worker = worker
        self._stop_event = threading.Event()

    def run(self):
        self.controller = self.worker("COM4")

        while not self._stop_event.is_set():
            self.controller.send_major_color()

        self.controller.disconnect()

    def stop(self):
        self._stop_event.set()


class QTworkerThread(QThread):
    """
    This does not work... I may do more investigating later or just
    continue to use built in threading.
    Perhaps threading.event can be used with Qthread objects?
    """
    def __init__(self, worker):
        QThread.__init__(self)
        self.worker = worker

    def __del__(self):
        self.wait()

    def run(self):
        self.controller = self.worker('COM4')
        #print("starting")
        #while True:
            #time.sleep(1)
            #print("THis is happening!")

    def stop(self):
        print("Stopping")
        #self.controller.controlling = False
        print("disconnecting")
        #self.controller.disconnect()
        print("terminating")
        self.terminate()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    window = PyLightApp(main_window)
    main_window.show()
    sys.exit(app.exec_())