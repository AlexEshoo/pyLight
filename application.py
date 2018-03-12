import pyLight
from gui import Ui_MainWindow
import sys
import glob
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow


class PyLightApp(Ui_MainWindow):
    def __init__(self, main_window_object):
        # Ui_MainWindow.__init__(self)
        self.setupUi(main_window_object)
        self.controller = None

        self.populate_combo_boxes()
        self.connect_slots()

        self.com_port = self.serialPortComboBox.currentText()

    def connect_slots(self):
        self.applyButton.clicked.connect(self.do_apply)
        self.actionExit.triggered.connect(self.exit)

    def populate_combo_boxes(self):
        for key in pyLight.CONTROL_MODES:
            self.controlModeComboBox.addItem(key)

        for port in serial_ports():
            self.serialPortComboBox.addItem(port)

    def do_apply(self):
        control = self.controlModeComboBox.currentText()

        if self.controller:
            self.controller.release_control()

        self.com_port = self.serialPortComboBox.currentText()
        print(self.com_port)
        self.controller = pyLight.CONTROL_MODES[control](self.com_port)
        print("Beginning Control")
        self.controller.begin_control()

    def exit(self):
        if self.controller:
            self.controller.release_control()

        QApplication.quit()


def serial_ports():
    """
        Thanks to: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
        Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    window = PyLightApp(main_window)
    main_window.show()
    sys.exit(app.exec_())
