# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/documents/mageiasync/mageiaSync/mageiaSyncDBprefs.ui'
#
# Created: Sun Dec  7 13:24:26 2014
#      by: PyQt5 UI code generator 5.1.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_prefsDialog(object):
    def setupUi(self, prefsDialog):
        prefsDialog.setObjectName("prefsDialog")
        prefsDialog.resize(520, 234)
        self.buttonBox = QtWidgets.QDialogButtonBox(prefsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 200, 511, 32))
        self.buttonBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(prefsDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 501, 185))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.user = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.user.setToolTip("")
        self.user.setStatusTip("")
        self.user.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.user.setObjectName("user")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.user)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.password = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.password.setToolTip("")
        self.password.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.password.setObjectName("password")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.password)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.location = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.location.setToolTip("")
        self.location.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.location.setObjectName("location")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.location)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.selectDest = QtWidgets.QPushButton(self.formLayoutWidget)
        self.selectDest.setToolTip("")
        self.selectDest.setObjectName("selectDest")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.selectDest)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.bwl = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.bwl.setToolTip("")
        self.bwl.setMaximum(100000)
        self.bwl.setSingleStep(50)
        self.bwl.setObjectName("bwl")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.bwl)
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_7)
        self.release = QtWidgets.QComboBox(self.formLayoutWidget)
        self.release.setEditable(True)
        self.release.setObjectName("release")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.release)

        self.retranslateUi(prefsDialog)
        self.buttonBox.accepted.connect(prefsDialog.accept)
        self.buttonBox.rejected.connect(prefsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(prefsDialog)

    def retranslateUi(self, prefsDialog):
        _translate = QtCore.QCoreApplication.translate
        prefsDialog.setWindowTitle(_translate("prefsDialog", "Preferences"))
        self.label.setToolTip(_translate("prefsDialog", "Give the release name like \"mageia5-alpha2\""))
        self.label.setText(_translate("prefsDialog", "Release:"))
        self.label_2.setToolTip(_translate("prefsDialog", "User name to acces the repository. Only for testing repository."))
        self.label_2.setText(_translate("prefsDialog", "User:"))
        self.label_3.setToolTip(_translate("prefsDialog", "Associated with user, if needed"))
        self.label_3.setText(_translate("prefsDialog", "Password:"))
        self.label_4.setToolTip(_translate("prefsDialog", "Source repository. Keep void to use the testing repo."))
        self.label_4.setText(_translate("prefsDialog", "Source:"))
        self.label_5.setToolTip(_translate("prefsDialog", "The local directory where you store ISOs. Will sync your existent ISOs already present."))
        self.label_5.setText(_translate("prefsDialog", "Destination:"))
        self.selectDest.setText(_translate("prefsDialog", "PushButton"))
        self.label_6.setToolTip(_translate("prefsDialog", "Set to zero if you don\'t want apply limit."))
        self.label_6.setText(_translate("prefsDialog", "Bandwith limit (kB/s):"))
        self.label_7.setText(_translate("prefsDialog", "Define parameters which are stored and used for rsync"))

