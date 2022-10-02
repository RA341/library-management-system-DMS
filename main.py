from re import S
import sys
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QCompleter, QComboBox, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from database import mysqlDB
from main_UI import Ui_main_view

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
        self.GetUsersData()
        self.GetBooksData()
        self.GetIssuedData()

        # Initialing all pages
        self.MainPage()
        self.IssuePage()
        self.ReturnPage()
        self.BooksPage()
        self.UsersPage()
        self.BookStatusPage()

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
        
        # Users page
        self.users_page_back_button = self.ui.user_back_button
        self.user_table = self.ui.user_tableWidget

        # Book Status page
        self.bk_status_back_button = self.ui.book_status_back_button
    
    def MainPage(self):
        self.issue_button.clicked.connect(self.goto_issue_page)
        self.return_button.clicked.connect(self.goto_return_page)
        self.books_button.clicked.connect(self.goto_book_page)
        self.users_button.clicked.connect(self.goto_user_page)
        self.bk_status_button.clicked.connect(self.goto_BookStatus_page)
    def IssuePage(self):
        # Getting late user and books list
        self.GetBooksData()
        self.GetUsersData()

        self.issue_page_back_button.clicked.connect(self.goto_main_page)
        self.issue_page_book_combo_box.activated.connect(self.BookComboAction)
        self.issue_page_user_combo_box.activated.connect(self.UserComboAction)
        self.BookComboBoxData()
        self.UsersComboBoxData()
        self.issue_page_user_combo_box.addItems(self.users)
        self.issue_page_book_combo_box.addItems(self.books)

        self.issue_page_book_combo_box.setEditable(True)
        self.issue_page_book_combo_box.setDuplicatesEnabled(False)
        self.issue_page_book_combo_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.issue_page_book_combo_box.setInsertPolicy(QComboBox.NoInsert)

        self.issue_page_user_combo_box.setEditable(True)
        self.issue_page_user_combo_box.setDuplicatesEnabled(False)
        self.issue_page_user_combo_box.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.issue_page_user_combo_box.setInsertPolicy(QComboBox.NoInsert)

        self.issue_page_confirm_button.clicked.connect(self.ConfirmIssue)
        self.issue_page_book_combo_box.currentTextChanged.connect(self.BookComboAction)
        self.issue_page_user_combo_box.currentTextChanged.connect(self.UserComboAction)
        self.issue_page_datedit.setCalendarPopup(True)
        today = QDate().currentDate()
        self.issue_page_datedit.setDate(today)
        self.issue_page_return_day_spinbox.textChanged.connect(self.SetReturnDate)
        retun = self.issue_page_datedit.date().addDays(self.issue_page_return_day_spinbox.value()).toPyDate()
        self.issue_page_return_date_label.setText(str(retun.day) + "-" + str(retun.month) + "-" + str(retun.year))

    def ReturnPage(self):
        self.return_page_back_button.clicked.connect(self.goto_main_page)

    def BooksPage(self):
        self.books_page_back_button.clicked.connect(self.goto_main_page)
        self.LoadBooksData()

    def UsersPage(self):
        self.users_page_back_button.clicked.connect(self.goto_main_page)
        self.LoadUsersData()

    def BookStatusPage(self):
        self.bk_status_back_button.clicked.connect(self.goto_main_page)

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
        self.issued_books = [x for x in self.cursor.fetchall()]

    # table data for user and books page
    def LoadBooksData(self):
        self.GetBooksData()
        self.GetBookColumns()

        # Modifying list
        del self.books_column_names[3]
        self.books_column_names[1] = "Book Name"
        self.books_column_names[2] = "Author Name"

        # Adding columns to table
        self.book_table.setRowCount(len(self.books_list))
        self.book_table.setColumnCount(len(self.books_column_names))
        self.book_table.setHorizontalHeaderLabels(self.books_column_names)
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

        self.GetUserColumns()
        self.GetUsersData()

        del self.users_column_names[2]
        self.users_column_names[0] = "User ID"
        self.users_column_names[1] = "User Name"

        self.user_table.setRowCount(len(self.user_list))
        self.user_table.setColumnCount(len(self.users_column_names))
        self.user_table.setHorizontalHeaderLabels(self.users_column_names)

        header = self.user_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        row = 0

        for user in self.user_list:
            self.user_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.user_table.setItem(row, 1, QtWidgets.QTableWidgetItem(user[1] + " " + user[2]))
            self.user_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user[3])))
            row += 1

    # issue page functions
    def UserComboAction(self):
        self.GetUsersData()
        user_name_dict = dict([(str(x[0]), x[1] + " " + x[2]) for x in self.user_list])
        user = user_name_dict.get(self.issue_page_user_combo_box.currentText())
        if user:
            self.issue_page_user_label.setText(user)
        else:
            self.issue_page_user_label.setText("Invalid input")

    def BookComboAction(self):
        self.GetBooksData()
        book_name_dict = dict([(str(x[0]), x[1]) for x in self.books_list])
        book = book_name_dict.get(self.issue_page_book_combo_box.currentText())
        if book:
            self.issue_page_book_label.setText(book)
        else:
            self.issue_page_book_label.setText("Invalid input")

    def ConfirmIssue(self):
        bookID = self.issue_page_book_combo_box.currentText()
        userID = self.issue_page_user_combo_box.currentText()
        issue = str(self.issue_page_datedit.date().toPyDate())
        retun = str(self.issue_page_datedit.date().addDays(self.issue_page_return_day_spinbox.value()).toPyDate())
        query = "insert into issued values (%s,%s,%s,%s)"
        data = (bookID, userID, issue, retun)
        try:
            self.cursor.execute(query, data)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Successful operation")
            msg.setInformativeText("Record added Successfully")
            msg.setWindowTitle("Success")
            msg.exec_()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()

    def SetReturnDate(self):
        retun = self.issue_page_datedit.date().addDays(self.issue_page_return_day_spinbox.value()).toPyDate()
        self.issue_page_return_date_label.setText(str(retun.day) + "-" + str(retun.month) + "-" + str(retun.year))

    def BookComboBoxData(self):
        self.GetIssuedData()
        self.GetBooksData()
        self.allowed_books = []
        for y in self.books_list:
            if y[0] not in self.issued_books:
                self.allowed_books.append(y)
        print(self.allowed_books)
        self.books = [str(x[0]) for x in self.allowed_books]
        self.last_books = self.books

    def UsersComboBoxData(self):
        self.users = [str(x[0]) for x in self.user_list]
        self.last_users = self.users

    # Main page elements
    def goto_issue_page(self):
        self.BookComboBoxData()
        self.UsersComboBoxData()
        print(self.books)
        print(self.last_books)
        if self.books != self.last_books:
            self.issue_page_user_combo_box.addItems(self.users)
        if self.users != self.last_users:
            self.issue_page_book_combo_box.addItems(self.books)
        self.ui.stackedWidget.setCurrentWidget(self.ui.issue_page)

    def goto_return_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.return_page)

    def goto_book_page(self):
        self.LoadBooksData()
        self.ui.stackedWidget.setCurrentWidget(self.ui.book_page)

    def goto_user_page(self):
        self.LoadUsersData()
        self.ui.stackedWidget.setCurrentWidget(self.ui.user_page)

    def goto_BookStatus_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.book_status_page)

    # Issue page elements
    def goto_main_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

    # Books list


#####################################

#####################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.showUI()
    sys.exit(app.exec_())
