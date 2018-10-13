# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clarafai.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
import cv2 as cv
import os
import time
from clarifai.rest import ClarifaiApp

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(2046, 1367)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(820, 1260, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(1020, 100, 971, 981))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)

        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(190, 1150, 1781, 81))
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(140, 240, 691, 701))
        self.label_8.setObjectName("label_8")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        image = QPixmap("scene.jpg")
        image = image.scaledToWidth(300)
        image = image.scaledToHeight(300)
        self.label.setPixmap(image)

        image2 = QPixmap("scene.jpg")
        image2 = image2.scaledToWidth(300)
        image2 = image2.scaledToHeight(300)
        self.label_2.setPixmap(image2)

        image3 = QPixmap("scene.jpg")
        image3 = image3.scaledToWidth(300)
        image3 = image3.scaledToHeight(300)
        self.label_3.setPixmap(image3)

        image4 = QPixmap("scene.jpg")
        image4 = image4.scaledToWidth(300)
        image4 = image4.scaledToHeight(300)
        self.label_4.setPixmap(image4)

        image5 = QPixmap("scene.jpg")
        image5 = image5.scaledToWidth(300)
        image5 = image5.scaledToHeight(300)
        self.label_5.setPixmap(image5)


        image6 = QPixmap("scene.jpg")
        image6 = image6.scaledToWidth(300)
        image6 = image6.scaledToHeight(300)
        self.label_6.setPixmap(image6)

        self.label_7.setText(_translate("Dialog", "Top Searches"))
        self.label_8.setText(_translate("Dialog", "SCRNSHT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
