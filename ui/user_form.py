# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'I:\School project(dms,sdoop)\user_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class UserDialogUi(object):
    def setupUi(self, user_dialog):
        user_dialog.setObjectName("user_dialog")
        user_dialog.resize(700, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(user_dialog.sizePolicy().hasHeightForWidth())
        user_dialog.setSizePolicy(sizePolicy)
        self.user_phone = QtWidgets.QLineEdit(user_dialog)
        self.user_phone.setGeometry(QtCore.QRect(150, 150, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.user_phone.setFont(font)
        self.user_phone.setObjectName("user_phone")
        self.label_2 = QtWidgets.QLabel(user_dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 150, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.user_form_cancel = QtWidgets.QPushButton(user_dialog)
        self.user_form_cancel.setGeometry(QtCore.QRect(410, 340, 151, 41))
        self.user_form_cancel.setObjectName("user_form_cancel")
        self.user_lname_input = QtWidgets.QLineEdit(user_dialog)
        self.user_lname_input.setGeometry(QtCore.QRect(488, 59, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.user_lname_input.setFont(font)
        self.user_lname_input.setObjectName("user_lname_input")
        self.user_fname_input = QtWidgets.QLineEdit(user_dialog)
        self.user_fname_input.setGeometry(QtCore.QRect(150, 60, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.user_fname_input.setFont(font)
        self.user_fname_input.setObjectName("user_fname_input")
        self.label_3 = QtWidgets.QLabel(user_dialog)
        self.label_3.setGeometry(QtCore.QRect(356, 58, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(user_dialog)
        self.label.setGeometry(QtCore.QRect(20, 59, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.user_form_confirm = QtWidgets.QPushButton(user_dialog)
        self.user_form_confirm.setGeometry(QtCore.QRect(170, 340, 151, 41))
        self.user_form_confirm.setObjectName("user_form_confirm")

        self.retranslateUi(user_dialog)
        QtCore.QMetaObject.connectSlotsByName(user_dialog)

    def retranslateUi(self, user_dialog):
        _translate = QtCore.QCoreApplication.translate
        user_dialog.setWindowTitle(_translate("user_dialog", "Dialog"))
        self.label_2.setText(_translate("user_dialog", "Phone No"))
        self.user_form_cancel.setText(_translate("user_dialog", "Cancel"))
        self.label_3.setText(_translate("user_dialog", "Last Name"))
        self.label.setText(_translate("user_dialog", "First Name"))
        self.user_form_confirm.setText(_translate("user_dialog", "Confirm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    user_dialog = QtWidgets.QDialog()
    ui = UserDialogUi()
    ui.setupUi(user_dialog)
    user_dialog.show()
    sys.exit(app.exec_())