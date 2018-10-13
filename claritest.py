from PyQt5 import QtCore, QtGui, QtWidgets, uic

class MyWindow(QTWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('clarafai.ui', self)

    if __name__ == '__main__':
        import FONT_HERSHEY_SIMPLEXapp = QtWidgets.QApplication(sys.argv)
        window = MyWindow()
        window.show()
        sys.exit(app.exec_)
