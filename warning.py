from PyQt5 import QtWidgets


def ignore_complete():
    msg = QtWidgets.QMessageBox()
    #icon Critical,Warning,Information,Question
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Ignore successfully")
    msg.exec_()   