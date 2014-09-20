# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mageiaSyncDBprefs0.ui'
#
# Created: Sat Sep 20 21:16:42 2014
#      by: PyQt5 UI code generator 5.1.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_prefsDialog0(object):
    def setupUi(self, prefsDialog0):
        prefsDialog0.setObjectName("prefsDialog0")
        prefsDialog0.resize(520, 171)
        self.buttonBox = QtWidgets.QDialogButtonBox(prefsDialog0)
        self.buttonBox.setGeometry(QtCore.QRect(10, 130, 511, 32))
        self.buttonBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(prefsDialog0)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 501, 111))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_7)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.user = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.user.setToolTip("")
        self.user.setStatusTip("")
        self.user.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.user.setObjectName("user")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.user)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.password = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.password.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.password.setObjectName("password")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.password)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.location = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.location.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.location.setObjectName("location")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.location)

        self.retranslateUi(prefsDialog0)
        self.buttonBox.accepted.connect(prefsDialog0.accept)
        self.buttonBox.rejected.connect(prefsDialog0.reject)
        QtCore.QMetaObject.connectSlotsByName(prefsDialog0)

    def retranslateUi(self, prefsDialog0):
        _translate = QtCore.QCoreApplication.translate
        prefsDialog0.setWindowTitle(_translate("prefsDialog0", "Preferences"))
        self.label_7.setText(_translate("prefsDialog0", "Define parameters which are stored and used for rsync"))
        self.label_2.setToolTip(_translate("prefsDialog0", "User name to acces the repository. Only for testing repository."))
        self.label_2.setText(_translate("prefsDialog0", "User:"))
        self.label_3.setToolTip(_translate("prefsDialog0", "Associated with user, if needed"))
        self.label_3.setText(_translate("prefsDialog0", "Password:"))
        self.password.setToolTip(_translate("prefsDialog0", "Give a value if you want to use testing repository"))
        self.label_4.setToolTip(_translate("prefsDialog0", "Source repository. Keep void to use the testing repo."))
        self.label_4.setText(_translate("prefsDialog0", "Source:"))
        self.location.setToolTip(_translate("prefsDialog0", "Give a mirror adress with public access"))

