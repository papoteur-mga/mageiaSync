# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mageiaSyncDBrename.ui'
#
# Created: Tue Aug 26 07:25:27 2014
#      by: PyQt5 UI code generator 5.1.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_renameDialog(object):
    def setupUi(self, renameDialog):
        renameDialog.setObjectName("renameDialog")
        renameDialog.resize(562, 138)
        self.buttonBox = QtWidgets.QDialogButtonBox(renameDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 100, 541, 32))
        self.buttonBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(renameDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 556, 100))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.oldRelease = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.oldRelease.setObjectName("oldRelease")
        self.gridLayout.addWidget(self.oldRelease, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.newRelease = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.newRelease.setObjectName("newRelease")
        self.gridLayout.addWidget(self.newRelease, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.chooseDir = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.chooseDir.setObjectName("chooseDir")
        self.gridLayout.addWidget(self.chooseDir, 1, 1, 1, 1)

        self.retranslateUi(renameDialog)
        self.buttonBox.accepted.connect(renameDialog.accept)
        self.buttonBox.rejected.connect(renameDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(renameDialog)

    def retranslateUi(self, renameDialog):
        _translate = QtCore.QCoreApplication.translate
        renameDialog.setWindowTitle(_translate("renameDialog", "Rename release"))
        self.label.setText(_translate("renameDialog", "Old release"))
        self.label_2.setText(_translate("renameDialog", "New release"))
        self.label_3.setText(_translate("renameDialog", "This action renames the directories and names from a former version to a new one."))
        self.label_4.setText(_translate("renameDialog", "TextLabel"))
        self.chooseDir.setText(_translate("renameDialog", "PushButton"))

