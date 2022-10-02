import random
from re import S
import sys
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QCompleter, QComboBox, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from database import mysqlDB
from main_UI import Ui_main_view
from user_form import Ui_user_form
from book_form import Ui_book_form

# ui conversion code
# pyuic5 -x "I:\School project(dms,sdoop)\library_database_management.ui" -o main_UI.py

"""
ToDo - create add and delete functions for table widgets
ToDo - create popup view for inputing books and users
"""


class MainWindow:
    def __init__(self):
        # Initializing main app window
        self.main_win = QMainWindow()
        self.main_win.setFixedSize(1000, 800)

        # Adding ui file
        self.ui = Ui_main_view()
        self.ui.setupUi(self.main_win)

        # Initializing Mysql Cursor
        self.sql = mysqlDB()
        self.cursor = self.sql.dbcursor

        # Initializing UI
        self.ui_elements()
        # Setting Main Page
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

        # Initilizing books,users,issued lists
        self.GetUserColumns()
        self.GetUsersData()

        self.GetBookColumns()
        self.GetBooksData()

        self.GetIssuedColumns()
        self.GetIssuedData()

        self.GetAllowedBooks()

        # Initialing all pages
        self.MainPage()
        self.IssuePage()
        self.ReturnPage()
        self.BooksPage()
        self.UsersPage()
        self.BookStatusPage()

    ###############################################################################################################
    def showUI(self):
        self.main_win.show()

    def ui_elements(self):
        # Home Page
        self.issue_button = self.ui.issue_button
        self.return_button = self.ui.return_button
        self.books_button = self.ui.book_button
        self.users_button = self.ui.user_button
        self.bk_status_button = self.ui.book_status_button

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

        # Return Page
        self.return_page_back_button = self.ui.return_back_button

        # Book Page
        self.books_page_back_button = self.ui.book_back_Button
        self.book_table = self.ui.book_tableWidget
        self.book_add_book = self.ui.addBook_pushButton
        self.book_remove_book = self.ui.delBook_pushButton

        # Users page
        self.users_page_back_button = self.ui.user_back_button
        self.user_table = self.ui.user_tableWidget
        self.user_add_user = self.ui.addUser_pushButton
        self.user_remove_user = self.ui.delUser_pushButton

        # Book Status page
        self.bk_status_back_button = self.ui.book_status_back_button
        self.bk_issued_table = self.ui.bookStatus_tableWidget

    ###############################################################################################################
    def MainPage(self):
        self.issue_button.clicked.connect(self.goto_issue_page)
        self.return_button.clicked.connect(self.goto_return_page)
        self.books_button.clicked.connect(self.goto_book_page)
        self.users_button.clicked.connect(self.goto_user_page)
        self.bk_status_button.clicked.connect(self.goto_BookStatus_page)

    def IssuePage(self):
        self.issue_page_back_button.clicked.connect(self.goto_main_page)
        # combobox on change functions
        self.issue_page_book_combo_box.activated.connect(self.IssueComboAction)
        self.issue_page_user_combo_box.activated.connect(self.IssueComboAction)

        # setting properties for book combobox
        self.issue_page_book_combo_box.setEditable(True)
        self.issue_page_book_combo_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.issue_page_book_combo_box.setInsertPolicy(QComboBox.NoInsert)

        # setting properties for user combobox
        self.issue_page_user_combo_box.setEditable(True)
        self.issue_page_user_combo_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.issue_page_user_combo_box.setInsertPolicy(QComboBox.NoInsert)

        # confirm button inits
        self.issue_page_confirm_button.clicked.connect(self.ConfirmIssue)
        self.issue_page_book_combo_box.currentTextChanged.connect(self.IssueComboAction)
        self.issue_page_user_combo_box.currentTextChanged.connect(self.IssueComboAction)
        self.issue_page_datedit.setCalendarPopup(True)
        today = QDate().currentDate()
        self.issue_page_datedit.setDate(today)

        self.issue_page_return_day_spinbox.textChanged.connect(self.SetReturnDate)
        self.return_days = self.issue_page_datedit.date().addDays(self.issue_page_return_day_spinbox.value()).toPyDate()
        self.issue_page_return_date_label.setText(
            str(self.return_days.day) + "-" + str(self.return_days.month) + "-" + str(self.return_days.year))

    def ReturnPage(self):
        self.return_page_back_button.clicked.connect(self.goto_main_page)

    def BooksPage(self):
        self.book_add_book.clicked.connect(self.AddBooks)
        self.book_remove_book.clicked.connect(self.DelBooks)
        self.books_page_back_button.clicked.connect(self.goto_main_page)

    def UsersPage(self):
        self.users_page_back_button.clicked.connect(self.goto_main_page)

    def BookStatusPage(self):
        self.bk_status_back_button.clicked.connect(self.goto_main_page)

    ###############################################################################################################

    ###############################################################################################################
    # User and book lists function
    def GetBookColumns(self):
        self.cursor.execute("show columns from books")
        self.books_column_names = [x[0] for x in self.cursor.fetchall()]

    def GetBooksData(self):
        self.cursor.execute("select * from books")
        self.books_list = [x for x in self.cursor.fetchall()]

    def GetUserColumns(self):
        self.cursor.execute("show columns from users")
        self.users_column_names = [x[0] for x in self.cursor.fetchall()]

    def GetUsersData(self):
        self.cursor.execute("select * from users")
        self.user_list = [x for x in self.cursor.fetchall()]

    def GetIssuedColumns(self):
        self.cursor.execute("show columns from issued")
        self.issued_column_names = [x[0] for x in self.cursor.fetchall()]

    def GetIssuedData(self):
        self.cursor.execute("select * from issued")
        self.issued_list = [x for x in self.cursor.fetchall()]

    def GetAllowedBooks(self):
        self.allowed_books = [y for y in self.books_list if y[0] not in [x[0] for x in self.issued_list]]
        # print("allowed", self.allowed_books)
        # print("book",self.books_list)
        # print("issue",self.issued_list)

    def RefreshLists(self):
        print("executing refresh")
        self.GetUsersData()
        self.GetBooksData()
        self.GetIssuedData()
        self.GetAllowedBooks()

    ###############################################################################################################

    ###############################################################################################################
    # table data for user and books page
    def LoadBooksData(self):
        books_column_copy = self.books_column_names.copy()
        # Modifying list
        del books_column_copy[3]
        books_column_copy[1] = "Book Name"
        books_column_copy[2] = "Author Name"

        # Adding columns to table
        self.book_table.setRowCount(len(self.books_list))
        self.book_table.setColumnCount(len(books_column_copy))
        self.book_table.setHorizontalHeaderLabels(books_column_copy)
        # resizing columns
        header = self.book_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        # adding data into tables
        row = 0

        for book in self.books_list:
            self.book_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(book[0])))
            self.book_table.setItem(row, 1, QtWidgets.QTableWidgetItem(book[1]))
            self.book_table.setItem(row, 2, QtWidgets.QTableWidgetItem(book[2] + " " + book[3]))

            row += 1

    def LoadUsersData(self):
        user_column_copy = self.users_column_names.copy()

        del user_column_copy[2]
        user_column_copy[0] = "User ID"
        user_column_copy[1] = "User Name"
        user_column_copy[2] = "Phone No"
        # print(self.users_column_names)
        # print(user_column_copy)

        self.user_table.setRowCount(len(self.user_list))
        self.user_table.setColumnCount(len(user_column_copy))
        self.user_table.setHorizontalHeaderLabels(user_column_copy)

        header = self.user_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        row = 0

        for user in self.user_list:
            self.user_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.user_table.setItem(row, 1, QtWidgets.QTableWidgetItem(user[1] + " " + user[2]))
            self.user_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user[2])))
            row += 1

    def LoadIssuedData(self):
        # Modifying list
        self.issued_column_names[1] = "User ID"
        self.issued_column_names[2] = "Issue Date"
        self.issued_column_names[3] = "Return Date"

        # Adding columns to table
        self.bk_issued_table.setRowCount(len(self.issued_list))
        self.bk_issued_table.setColumnCount(len(self.issued_column_names))
        self.bk_issued_table.setHorizontalHeaderLabels(self.issued_column_names)
        # resizing columns
        header = self.bk_issued_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        # adding data into tables
        row = 0

        for book in self.issued_list:
            self.bk_issued_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(book[0])))
            self.bk_issued_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(book[1])))
            self.bk_issued_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(book[2])))
            self.bk_issued_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(book[3])))

            row += 1

    def AddBooks(self):
        self.w = UserForm()
        self.w.show()

    def DelBooks(self):
        try:
            index = self.book_table.currentRow()
            if index > -1:
                query = "delete from books where ISBN = %s"
                data = (self.book_table.item(index, 0).text(),)
                self.cursor.execute(query, data)
                self.ShowInfoMessage("Record successfully deleted", "Success", "Record deleted")
                self.RefreshLists()
                self.goto_book_page()
            else:
                ShowErrorMessage("No item selected", "Item error", "Item not found")
        except Exception as e:
            print("del", e)

    ###############################################################################################################

    ###############################################################################################################
    # issue page functions
    def IssueComboAction(self):
        try:
            user_name_dict = dict([(str(x[0]), x[1] + " " + x[2]) for x in self.user_list])
            user = user_name_dict.get(self.issue_page_user_combo_box.currentText())

            book_name_dict = dict([(str(x[0]), x[1]) for x in self.books_list])
            book = book_name_dict.get(self.issue_page_book_combo_box.currentText())

            if book and user:
                self.issue_page_book_label.setText(book)
                self.issue_page_user_label.setText(user)
                self.issue_page_confirm_button.setEnabled(True)
            else:
                self.issue_page_book_label.setText("Invalid input")
                self.issue_page_user_label.setText("Invalid input")
                self.issue_page_confirm_button.setEnabled(False)
        except Exception as e:
            print(e)

    def ConfirmIssue(self):
        bookID = self.issue_page_book_combo_box.currentText()
        userID = self.issue_page_user_combo_box.currentText()
        issue = str(self.issue_page_datedit.date().toPyDate())
        query = "insert into issued values (%s,%s,%s,%s)"
        data = (bookID, userID, issue, self.return_days)
        try:
            self.cursor.execute(query, data)
            self.RefreshLists()
            self.goto_issue_page()
            ShowInfoMessage("Record successfully added", "Success", "Item added")
        except Exception as e:
            ShowErrorMessage(str(e), "Error", "Error")

    def SetReturnDate(self):
        self.return_days = self.issue_page_datedit.date().addDays(self.issue_page_return_day_spinbox.value()).toPyDate()
        self.issue_page_return_date_label.setText(
            str(self.return_days.day) + "-" + str(self.return_days.month) + "-" + str(self.return_days.year))

    ###############################################################################################################

    ###############################################################################################################
    # Page navigation functions
    def goto_issue_page(self):
        try:
            books = [str(x[0]) for x in self.allowed_books]
            users = [str(x[0]) for x in self.user_list]
            # print("books", self.books)
            # print(self.last_books)

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
            print(e)

    def goto_return_page(self):
        try:
            self.ui.stackedWidget.setCurrentWidget(self.ui.return_page)
        except Exception as e:
            print(e)

    def goto_book_page(self):
        try:
            self.LoadBooksData()
            self.ui.stackedWidget.setCurrentWidget(self.ui.book_page)
        except Exception as e:
            print(e)

    def goto_user_page(self):
        try:
            self.LoadUsersData()
            self.ui.stackedWidget.setCurrentWidget(self.ui.user_page)
        except Exception as e:
            print(e)

    def goto_BookStatus_page(self):
        try:
            self.LoadIssuedData()
            self.ui.stackedWidget.setCurrentWidget(self.ui.book_status_page)
        except Exception as e:
            print(e)

    # Issue page elements
    def goto_main_page(self):
        try:
            self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)
        except Exception as e:
            print(e)

    ###############################################################################################################
    # message box functions


def ShowErrorMessage(message, win_title, title):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(win_title)
    msg.setText(title)
    msg.setInformativeText(message)
    msg.exec_()


def ShowInfoMessage(message, win_title, title):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(win_title)
    msg.setText(title)
    msg.setInformativeText(message)
    msg.exec_()


class UserForm(MainWindow):
    def __init__(self):
        # Initializing main app window
        super().__init__()
        self.main_win = QMainWindow()
        self.main_win.setFixedSize(700, 500)

        # Adding ui file
        self.ui = Ui_user_form()
        self.ui.setupUi(self.main_win)

        # conncecting buttons
        self.ui.user_form_confirm.clicked.connect(self.submit_user_info)
        self.ui.user_form_cancel.clicked.connect(lambda _: self.main_win.close())

    def submit_user_info(self):
        try:
            uid = self.gen_uid()
            while uid in [x[0] for x in self.user_list]:
                uid = self.gen_uid()
            fname = self.ui.user_fname_input.text()
            lname = self.ui.user_lname_input.text()
            phone = self.ui.user_phone.text()

            if len(fname) <= 1 or len(lname) <= 1:
                ShowErrorMessage("Name cannot be empty", "Name Error", "Invalid Name")
            elif len(phone) != 10 and type(phone) != int:
                ShowErrorMessage("Enter a valid phone number", "Phone Number Error",
                                 "Invalid Phone Number")
            else:
                data = (uid, fname, lname, phone)
                query = "insert into users values (%s,%s,%s,%s)"
                self.cursor.execute(query, data)
                ShowInfoMessage("Record added successfully", "Success", "Record Added")
                self.main_win.close()
        except Exception as e:
            print(e)

    def show(self):
        self.main_win.show()

    def gen_uid(self):
        return random.randrange(1000000000, 9999999999)


###############################################################################################################

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        main_win = MainWindow()
        main_win.showUI()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
