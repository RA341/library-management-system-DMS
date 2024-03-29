# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'I:\School project(dms,sdoop)\dms\ui files\book_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class BookDialogUi(object):
    def setupUi(self, book_dialog):
        book_dialog.setObjectName("book_dialog")
        book_dialog.resize(700, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(book_dialog.sizePolicy().hasHeightForWidth())
        book_dialog.setSizePolicy(sizePolicy)
        self.isbn_input = QtWidgets.QLineEdit(book_dialog)
        self.isbn_input.setGeometry(QtCore.QRect(510, 120, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.isbn_input.setFont(font)
        self.isbn_input.setObjectName("isbn_input")
        self.auth_fname_input = QtWidgets.QLineEdit(book_dialog)
        self.auth_fname_input.setGeometry(QtCore.QRect(160, 221, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.auth_fname_input.setFont(font)
        self.auth_fname_input.setObjectName("auth_fname_input")
        self.label_4 = QtWidgets.QLabel(book_dialog)
        self.label_4.setGeometry(QtCore.QRect(380, 220, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.book_form_confirm = QtWidgets.QPushButton(book_dialog)
        self.book_form_confirm.setGeometry(QtCore.QRect(150, 330, 151, 41))
        self.book_form_confirm.setObjectName("book_form_confirm")
        self.book_form_cancel = QtWidgets.QPushButton(book_dialog)
        self.book_form_cancel.setGeometry(QtCore.QRect(410, 330, 151, 41))
        self.book_form_cancel.setObjectName("book_form_cancel")
        self.label_2 = QtWidgets.QLabel(book_dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 220, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(book_dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 120, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.auth_lname_input = QtWidgets.QLineEdit(book_dialog)
        self.auth_lname_input.setGeometry(QtCore.QRect(510, 220, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.auth_lname_input.setFont(font)
        self.auth_lname_input.setText("")
        self.auth_lname_input.setObjectName("auth_lname_input")
        self.label = QtWidgets.QLabel(book_dialog)
        self.label.setGeometry(QtCore.QRect(400, 120, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.book_name_input = QtWidgets.QLineEdit(book_dialog)
        self.book_name_input.setGeometry(QtCore.QRect(160, 120, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.book_name_input.setFont(font)
        self.book_name_input.setText("")
        self.book_name_input.setObjectName("book_name_input")
        self.form_title = QtWidgets.QLabel(book_dialog)
        self.form_title.setGeometry(QtCore.QRect(180, 30, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.form_title.setFont(font)
        self.form_title.setAlignment(QtCore.Qt.AlignCenter)
        self.form_title.setObjectName("form_title")

        self.retranslateUi(book_dialog)
        QtCore.QMetaObject.connectSlotsByName(book_dialog)

    def retranslateUi(self, book_dialog):
        _translate = QtCore.QCoreApplication.translate
        book_dialog.setWindowTitle(_translate("book_dialog", " "))
        self.label_4.setText(_translate("book_dialog", "Author Last Name"))
        self.book_form_confirm.setText(_translate("book_dialog", "Confirm"))
        self.book_form_cancel.setText(_translate("book_dialog", "Cancel"))
        self.label_2.setText(_translate("book_dialog", "Author First Name"))
        self.label_3.setText(_translate("book_dialog", "Book Name"))
        self.label.setText(_translate("book_dialog", "ISBN"))
        self.form_title.setText(_translate("book_dialog", "Enter new book details"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    book_dialog = QtWidgets.QDialog()
    ui = Ui_book_dialog()
    ui.setupUi(book_dialog)
    book_dialog.show()
    sys.exit(app.exec_())
