import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, Qt, QObject


class WriteObject(QObject):
    write_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.write_signal.connect(self.worker, Qt.QueuedConnection)

    @pyqtSlot()
    def worker(self):
        print("Before sleep")
        time.sleep(2)
        print("After sleep")
        return True


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.CustomEvent = None
        self.write_thread = None
        self.init_ui()

    def init_ui(self):
        self.write_object = WriteObject()
        self.write_thread = QThread(self)
        self.write_thread.start()
        self.write_object.moveToThread(self.write_thread)

        redb = QPushButton("Red", self)
        redb.move(10, 10)

        blueb = QPushButton("Blue", self)
        blueb.move(10, 50)
        blueb.clicked.connect(self.print_method)

        redb.clicked.connect(self.send_event)

        self.setGeometry(300, 300, 300, 250)
        self.setWindowTitle("Toggle button")
        self.show()

    def send_event(self):
        print("\tSending signal")
        self.write_object.write_signal.emit()
        print("\tFinished sending signal")

    def print_method(self):
        print("Not frozen")


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ret = app.exec_()
    ex.write_thread.quit()
    ex.write_thread.wait()
    sys.exit(ret)


if __name__ == "__main__":
    main()