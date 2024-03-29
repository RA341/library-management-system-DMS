import random
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QCompleter, QComboBox, QMessageBox, QDialog

from database import MySqlDB
from ui.book_form import BookDialogUi
from ui.main_form import Ui_MainFormUi
from ui.user_form import UserDialogUi


class MainWindow:
    def __init__(self):
        # Initializing main app window
        self.main_win = QMainWindow()
        self.main_win.setFixedSize(1000, 800)
        self.main_win.setWindowTitle("Library Management System")

        # Adding ui file
        self.ui = Ui_MainFormUi()
        self.ui.setupUi(self.main_win)

        # Initializing Mysql Cursor
        self.sql = MySqlDB("librarydb")
        self.cursor = self.sql.dbcursor

        # Setting Main Page
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

        # Initializing books,users,issued lists
        self.getUserColumns()
        self.getBookColumns()
        self.getIssuedColumns()
        self.getDataLists()

        # Initialing all pages
        self.mainPage()
        self.issuePage()
        self.returnPage()
        self.booksPage()
        self.usersPage()
        self.bookStatusPage()

    ###############################################################################################################

    ###############################################################################################################
    def mainPage(self):
        # Home Page
        self.issue_button = self.ui.issue_button
        self.return_button = self.ui.return_button
        self.books_button = self.ui.book_button
        self.users_button = self.ui.user_button
        self.bk_status_button = self.ui.book_status_button

        self.issue_button.clicked.connect(self.goto_issue_page)
        self.return_button.clicked.connect(self.goto_return_page)
        self.books_button.clicked.connect(self.goto_book_page)
        self.users_button.clicked.connect(self.goto_user_page)
        self.bk_status_button.clicked.connect(self.goto_BookStatus_page)

    def issuePage(self):
        # Issue Page
        self.issue_page_back_button = self.ui.issue_back_button
        self.issue_page_user_combo_box = self.ui.issue_user_comboBox
        self.issue_page_book_combo_box = self.ui.issue_book_comboBox
        self.issue_page_user_label = self.ui.name_info_label
        self.issue_page_book_label = self.ui.book_info_label
        self.issue_page_datedit = self.ui.issue_dateEdit
        self.issue_page_return_day_spinbox = self.ui.day_spinBox
        self.issue_page_return_date_label = self.ui.return_date_label
        self.issue_page_confirm_button = self.ui.confirm_issue_pushButton

        self.issue_page_back_button.clicked.connect(self.goto_main_page)
        # combobox on change functions
        self.issue_page_book_combo_box.activated.connect(self.issueComboAction)
        self.issue_page_user_combo_box.activated.connect(self.issueComboAction)

        # setting properties for book combobox
        self.issue_page_book_combo_box.setEditable(True)
        self.issue_page_book_combo_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.issue_page_book_combo_box.setInsertPolicy(QComboBox.NoInsert)

        # setting properties for user combobox
        self.issue_page_user_combo_box.setEditable(True)
        self.issue_page_user_combo_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.issue_page_user_combo_box.setInsertPolicy(QComboBox.NoInsert)

        # confirm button inits
        self.issue_page_confirm_button.clicked.connect(self.confirmIssue)
        self.issue_page_book_combo_box.currentTextChanged.connect(self.issueComboAction)
        self.issue_page_user_combo_box.currentTextChanged.connect(self.issueComboAction)
        self.issue_page_datedit.setCalendarPopup(True)
        self.today = QDate().currentDate()
        self.issue_page_datedit.setDate(self.today)

        self.issue_page_datedit.dateChanged.connect(self.setReturnDate)
        self.issue_page_return_day_spinbox.textChanged.connect(self.setReturnDate)
        self.return_date = self.issue_page_datedit.date().addDays(self.issue_page_return_day_spinbox.value()).toPyDate()
        self.issue_page_return_date_label.setText(
            str(self.return_date.day) + "-" + str(self.return_date.month) + "-" + str(self.return_date.year))

    def returnPage(self):
        # Return Page
        # Info Labels
        self.return_name = self.ui.return_user
        self.return_book = self.ui.return_book
        self.return_issue_date = self.ui.issue_date
        self.return_return_date = self.ui.return_return_date
        self.return_days_late = self.ui.label_17
        self.return_total_fine = self.ui.label_22

        self.return_combo_box = self.ui.recipt_comboBox
        self.confirm_return = self.ui.confirm_return_pushButton
        self.return_page_back_button = self.ui.return_back_button

        self.return_combo_box.currentTextChanged.connect(self.returnComboBox)
        # setting properties for book combobox
        self.return_combo_box.setEditable(True)
        self.return_combo_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.return_combo_box.setInsertPolicy(QComboBox.NoInsert)
        self.confirm_return.clicked.connect(self.confirmReturn)
        self.return_page_back_button.clicked.connect(self.goto_main_page)

    def booksPage(self):
        # Book Page
        self.books_page_back_button = self.ui.book_back_Button

        self.book_table = self.ui.book_tableWidget
        self.book_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.book_add_book = self.ui.addBook_pushButton
        self.book_update_book = self.ui.upBook_pushButton
        self.book_remove_book = self.ui.delBook_pushButton

        self.book_add_book.clicked.connect(self.addBooks)
        self.book_update_book.clicked.connect(self.updateBooks)
        self.book_remove_book.clicked.connect(self.delBooks)

        self.books_page_back_button.clicked.connect(self.goto_main_page)

    def usersPage(self):
        # Users page
        self.users_page_back_button = self.ui.user_back_button

        self.user_table = self.ui.user_tableWidget
        self.user_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.user_add_user = self.ui.addUser_pushButton
        self.user_update_user = self.ui.upUser_pushButton
        self.user_remove_user = self.ui.delUser_pushButton

        self.user_add_user.clicked.connect(self.addUsers)
        self.user_update_user.clicked.connect(self.updateUsers)
        self.user_remove_user.clicked.connect(self.delUsers)

        self.users_page_back_button.clicked.connect(self.goto_main_page)

    def bookStatusPage(self):

        # Book Status page
        self.issued_back_button = self.ui.book_status_back_button
        self.issued_back_button.clicked.connect(self.goto_main_page)
        self.issue_refresh = self.ui.refreshlist_butt
        self.issue_refresh.clicked.connect(self.refreshfunc)
        self.issued_table = self.ui.bookStatus_tableWidget
        self.issued_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def refreshfunc(self):
        self.getDataLists()
        self.goto_BookStatus_page()

    ###############################################################################################################

    ###############################################################################################################
    # User and book lists function
    def getStoredProcedureData(self):
        for result in self.cursor.stored_results():
            return result.fetchall()

    def getBookColumns(self):
        self.cursor.callproc('getbookcolumnlist')
        tmp = self.getStoredProcedureData()
        self.books_column_names = [x[0] for x in tmp]

    def getBooksData(self):
        self.cursor.callproc("getbooklist")
        tmp = self.getStoredProcedureData()
        self.books_list = tmp
        self.book_name_dict = dict([(str(x[0]), [x[1], x[2]]) for x in self.books_list])

    def getUserColumns(self):
        self.cursor.callproc('getusercolumnlist')
        tmp = self.getStoredProcedureData()
        self.users_column_names = [x[0] for x in tmp]

    def getUsersData(self):
        self.cursor.callproc("getuserlist")
        tmp = self.getStoredProcedureData()
        self.user_list = tmp
        self.user_name_dict = dict([(str(x[0]), [x[1], x[2]]) for x in self.user_list])

    def getIssuedColumns(self):
        self.cursor.callproc("getissuedcolumnlist")
        tmp = self.getStoredProcedureData()
        self.issued_column_names = [x[0] for x in tmp]

    def getIssuedData(self):
        self.cursor.callproc("getissuedlist")
        tmp = self.getStoredProcedureData()
        self.issued_list = tmp
        self.issue_dict = dict([(str(x[0]), [x[1], x[2], x[3], x[4], x[5]]) for x in self.issued_list])

    def getAllowedBooks(self):
        self.cursor.callproc('getnonissuedbooklist')
        tmp = self.getStoredProcedureData()
        self.allowed_books = tmp

    def getDataLists(self):
        self.getUsersData()
        self.getBooksData()
        self.getIssuedData()
        self.getAllowedBooks()

    ###############################################################################################################

    ###############################################################################################################
    # table data and functions for user and books page
    def loadTableData(self, TableWidget, records_list: list, column_list):
        # Adding columns to table
        TableWidget.setRowCount(len(records_list))
        TableWidget.setColumnCount(len(column_list))
        TableWidget.setHorizontalHeaderLabels(column_list)

        # resizing columns
        header = TableWidget.horizontalHeader()
        for x in range(len(column_list)):
            header.setSectionResizeMode(x, QtWidgets.QHeaderView.Stretch)

        # adding data into tables
        for row, book in enumerate(records_list):
            for column, cell in enumerate(book):
                TableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(cell)))

    def addBooks(self):
        book_form = BookForm(book_list=self.books_list, cursor=self.cursor)
        book_form.exec()
        self.getDataLists()
        self.goto_book_page()

    def updateBooks(self):
        index = self.book_table.currentRow()
        if index > -1:
            data = (self.book_table.item(index, 0).text(),)
            if int(data[0]) in [x[0] for x in self.issued_list]:
                showErrorMessage("Return the book first", 'Error', 'Book cannot be altered')
            else:
                book_form = BookForm(book_list=self.book_name_dict, bid=data[0], cursor=self.cursor)
                book_form.exec()
                self.getDataLists()
                self.goto_book_page()
        else:
            showErrorMessage("No Book selected", "Item error", "Book not found")

    def delBooks(self):
        try:
            index = self.book_table.currentRow()
            if index > -1:
                data = (self.book_table.item(index, 0).text(),)
                if int(data[0]) in [x[0] for x in self.issued_list]:
                    showErrorMessage("Book is currently Issued", 'Error', 'Book cannot be deleted')
                else:
                    self.cursor.callproc('delbooks', data)
                    showInfoMessage("Book successfully deleted", "Success", "Record deleted")
                    self.getDataLists()
                    self.goto_book_page()
            else:
                showErrorMessage("No Book selected", "Item error", "Book not found")
        except Exception as delete:
            print("del", delete)

    def addUsers(self):
        user_form = UserForm(user_list=self.user_list, cursor=self.cursor)
        user_form.exec()
        self.getDataLists()
        self.goto_user_page()

    def updateUsers(self):
        try:
            index = self.user_table.currentRow()
            if index > -1:
                data = (self.user_table.item(index, 0).text(),)
                if int(data[0]) in [x[1] for x in self.issued_list]:
                    showErrorMessage("Member currently has Issued books\nReturn the books first", 'Error',
                                     'Member cannot be updated')
                else:
                    user_form = UserForm(user_list=self.user_name_dict, uid=data[0], cursor=self.cursor)
                    user_form.exec()
                    self.getDataLists()
                    self.goto_user_page()
            else:
                showErrorMessage("No Member selected", "Item error", "Member not found")
        except Exception as e:
            print("del", e)

    def delUsers(self):
        try:
            index = self.user_table.currentRow()
            if index > -1:
                data = (self.user_table.item(index, 0).text(),)
                if int(data[0]) in [x[1] for x in self.issued_list]:
                    showErrorMessage("Member currently has Issued books", 'Error', 'Member cannot be deleted')
                else:
                    self.cursor.callproc('deluser', data)
                    showInfoMessage("Member successfully deleted", "Success", "Record deleted")
                    self.getDataLists()
                    self.goto_user_page()
            else:
                showErrorMessage("No Member selected", "Item error", "Member not found")
        except Exception as e:
            print("del", e)

    ###############################################################################################################

    ###############################################################################################################
    # issue page functions
    def issueComboAction(self):
        try:
            user = self.user_name_dict.get(self.issue_page_user_combo_box.currentText())
            book = self.book_name_dict.get(self.issue_page_book_combo_box.currentText())

            if book:
                self.issue_page_book_label.setText(book[1])
            else:
                if len(self.allowed_books) == 0:
                    self.issue_page_book_label.setText("All books Issued")
                else:
                    self.issue_page_book_label.setText("Invalid input")

            if user:
                self.issue_page_user_label.setText(user[0])
            else:
                self.issue_page_user_label.setText("Invalid input")

            if book and user:
                self.issue_page_confirm_button.setEnabled(True)
            else:
                self.issue_page_confirm_button.setEnabled(False)
        except Exception as e:
            print(e)

    def confirmIssue(self):
        bookID = self.issue_page_book_combo_box.currentText()
        userID = self.issue_page_user_combo_box.currentText()
        issue = str(self.issue_page_datedit.date().toPyDate())
        data = (bookID, userID, issue, self.return_date)
        try:
            self.cursor.callproc('addissuebook', data)
            self.getDataLists()
            self.goto_issue_page()
            showInfoMessage("Book issued successfully", "Success", "Record added")

            self.issue_page_book_combo_box.setCurrentIndex(0)

            self.issue_page_user_combo_box.setCurrentIndex(0)
            self.issue_page_datedit.setDate(self.today)
            self.issue_page_return_day_spinbox.cleanText()

        except Exception as e:
            showErrorMessage(str(e), "Error", "Error")

    def setReturnDate(self):
        self.return_date = self.issue_page_datedit.date().addDays(self.issue_page_return_day_spinbox.value()).toPyDate()
        self.issue_page_return_date_label.setText(
            str(self.return_date.day) + "-" + str(self.return_date.month) + "-" + str(self.return_date.year))

    ###############################################################################################################

    ###############################################################################################################
    # Return Page functions

    def returnComboBox(self):
        data = self.issue_dict.get(self.return_combo_box.currentText())

        if data:
            try:
                self.return_name.setText(self.user_name_dict[str(data[0])][0])
                self.return_book.setText(self.book_name_dict[str(self.return_combo_box.currentText())][1])
                self.return_issue_date.setText(str(data[1].day) + "-" + str(data[1].month) + "-" + str(data[1].year))
                self.return_return_date.setText(str(data[2].day) + "-" + str(data[2].month) + "-" + str(data[2].year))
                self.return_days_late.setText(str(data[3]))
                self.return_total_fine.setText(str(data[4]))
            except Exception as e:
                print(e)

        else:
            self.return_name.setText("Invalid selection")

    def confirmReturn(self):
        try:
            isbn = self.return_combo_box.currentText()
            if isbn:
                data = (isbn,)
                self.cursor.callproc('delissued', data)
                showInfoMessage("Book returned successfully", "Success", "Record deleted")
                self.getDataLists()
                self.return_name.setText("")
                self.return_book.setText("")
                self.return_issue_date.setText("")
                self.return_return_date.setText("")
                self.return_days_late.setText("")
                self.return_total_fine.setText("")

                self.goto_return_page()
            else:
                showErrorMessage("No Book ID selected", "Item error", "Book not found")
        except Exception as e:
            print(e)

    ###############################################################################################################

    ###############################################################################################################
    # Page navigation functions
    def goto_issue_page(self):
        try:
            books = [str(x[0]) for x in self.allowed_books]
            users = [str(x[0]) for x in self.user_list]

            self.issue_page_book_combo_box.clear()
            self.issue_page_user_combo_box.clear()

            self.issue_page_user_combo_box.addItems(users)
            self.issue_page_book_combo_box.addItems(books)

            if self.issue_page_book_combo_box.currentIndex() < 0:
                self.issue_page_confirm_button.setEnabled(False)
            else:
                self.issue_page_confirm_button.setEnabled(True)

            self.ui.stackedWidget.setCurrentWidget(self.ui.issue_page)
        except Exception as e:
            print("Goto Issue Exceptions", e)

    def goto_return_page(self):
        try:
            issued = [str(x[0]) for x in self.issued_list]

            self.return_combo_box.clear()
            self.return_combo_box.addItems(issued)
            self.ui.stackedWidget.setCurrentWidget(self.ui.return_page)
        except Exception as e:
            print(e)

    def goto_book_page(self):
        try:
            self.loadTableData(self.book_table, self.books_list, self.books_column_names)
            self.ui.stackedWidget.setCurrentWidget(self.ui.book_page)
        except Exception as e:
            print(e)

    def goto_user_page(self):
        try:
            self.loadTableData(self.user_table, self.user_list, self.users_column_names)
            self.ui.stackedWidget.setCurrentWidget(self.ui.user_page)
        except Exception as e:
            print(e)

    def goto_BookStatus_page(self):
        try:
            self.loadTableData(self.issued_table, self.issued_list, self.issued_column_names)
            self.ui.stackedWidget.setCurrentWidget(self.ui.book_status_page)
        except Exception as e:
            print(e)

    # Issue page elements
    def goto_main_page(self):
        try:
            self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)
        except Exception as e:
            print(e)


################################################################################################################


# message box functions
def showErrorMessage(message, win_title, title):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(win_title)
    msg.setText(title)
    msg.setInformativeText(message)
    msg.exec_()


def showInfoMessage(message, win_title, title):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(win_title)
    msg.setText(title)
    msg.setInformativeText(message)
    msg.exec_()


################################################################################################################

class UserForm(QDialog):
    def __init__(self, parent=None, user_list=None, uid=None, cursor=None):
        # Initializing main app window
        super().__init__(parent)

        # Adding ui file
        self.ui = UserDialogUi()
        self.ui.setupUi(self)

        # getting book list and sql cursor
        self.user_list = user_list.copy()
        self.cursor = cursor

        # connecting buttons
        if isinstance(user_list, list):
            self.ui.user_form_confirm.clicked.connect(self.submitUserInfo)
        elif isinstance(user_list, dict):
            self.ui.form_title.setText("Update Member Details")
            self.ui.user_fname_input.setText(self.user_list[uid][0].split()[0])
            self.ui.user_lname_input.setText(self.user_list[uid][0].split()[1])
            self.ui.user_phone.setText(self.user_list[uid][1])
            self.ui.user_form_confirm.clicked.connect(lambda _: self.updateUserInfo(uid))

        self.ui.user_form_cancel.clicked.connect(lambda _: self.close())

    def submitUserInfo(self):
        try:
            uid = random.randrange(1000000000, 9999999999)
            while uid in [x[0] for x in self.user_list]:
                uid = random.randrange(1000000000, 9999999999)
            fname = self.ui.user_fname_input.text()
            lname = self.ui.user_lname_input.text()
            phone = self.ui.user_phone.text()

            if len(fname) <= 1 or len(lname) <= 1:
                showErrorMessage("Name cannot be empty", "Name Error", "Invalid Name")
            elif len(phone) != 10 and type(phone) != int:
                showErrorMessage("Enter a valid phone number (10 digits)", "Phone Number Error",
                                 "Invalid Phone Number")
            else:
                data = (uid, fname, lname, phone)
                self.cursor.callproc('adduser', data)
                showInfoMessage("Member added successfully", "Success", "Record Added")
                self.close()

        except Exception as e:
            print(e)

    def updateUserInfo(self, uid):
        try:
            fname = self.ui.user_fname_input.text()
            lname = self.ui.user_lname_input.text()
            phone = self.ui.user_phone.text()

            if len(fname) <= 1 or len(lname) <= 1:
                showErrorMessage("Name cannot be empty", "Name Error", "Invalid Name")
            elif len(phone) != 10 and type(phone) != int:
                showErrorMessage("Enter a valid phone number (10 digits)", "Phone Number Error",
                                 "Invalid Phone Number")
            else:
                data = (uid, fname, lname, phone)
                self.cursor.callproc('updateuser', data)
                showInfoMessage("Member updated successfully", "Success", "Record updated")
                self.close()

        except Exception as e:
            print(e)


#########################################################################

class BookForm(QDialog):
    def __init__(self, parent=None, book_list=None, bid=None, cursor=None):
        # Initializing main app window
        super().__init__(parent)

        # Adding ui file
        self.ui = BookDialogUi()
        self.ui.setupUi(self)

        # getting book list and sql cursor
        self.cursor = cursor
        self.books_list = book_list.copy()

        if isinstance(book_list, list):
            self.ui.book_form_confirm.clicked.connect(self.submitBookInfo)
        elif isinstance(book_list, dict):
            self.ui.isbn_input.setHidden(True)
            self.ui.label.setHidden(True)
            self.ui.form_title.setText("Update Book Details")
            self.ui.auth_fname_input.setText(self.books_list[bid][0].split()[0])
            self.ui.auth_lname_input.setText(self.books_list[bid][0].split()[1])
            self.ui.book_name_input.setText(self.books_list[bid][1])
            self.ui.book_form_confirm.clicked.connect(lambda _: self.updateBookInfo(bid))

        self.ui.book_form_cancel.clicked.connect(lambda _: self.close())

    def submitBookInfo(self):
        try:
            bid = self.ui.isbn_input.text()
            fname = self.ui.auth_fname_input.text()
            lname = self.ui.auth_lname_input.text()
            book_name = self.ui.book_name_input.text()

            if type(bid) != int and len(bid) != 13:
                showErrorMessage("ISBN is incorrect\nMake sure it is 13 digits only", "ISBN Error", "Invalid ISBN")
            elif int(bid) in [x[0] for x in self.books_list]:
                showErrorMessage("Book is already in database ", "ISBN Error", "ISBN exists")
            elif len(fname) <= 1 or len(lname) <= 1:
                showErrorMessage("Name cannot be empty", "Name Error", "Invalid Name")
            elif len(book_name) <= 1:
                showErrorMessage("Book Name cannot be empty", "Name Error", "Invalid Name")
            else:
                data = (bid, book_name, fname, lname)
                self.cursor.callproc('addbook', data)
                showInfoMessage("Record added successfully", "Success", "Record Added")
                self.close()
        except Exception as e:
            print(e)

    def updateBookInfo(self, bid):
        try:
            fname = self.ui.auth_fname_input.text()
            lname = self.ui.auth_lname_input.text()
            book_name = self.ui.book_name_input.text()

            if len(fname) <= 1 or len(lname) <= 1:
                showErrorMessage("Name cannot be empty", "Name Error", "Invalid Name")
            elif len(book_name) <= 1:
                showErrorMessage("Book Name cannot be empty", "Name Error", "Invalid Name")
            else:
                data = (bid, book_name, fname, lname)
                self.cursor.callproc('updatebook', data)
                showInfoMessage("Record updated successfully", "Success", "Record updated")
                self.close()
        except Exception as e:
            print(e)


###############################################################################################################

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        main_win = MainWindow()
        main_win.main_win.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
