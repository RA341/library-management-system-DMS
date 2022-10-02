from re import S
import sys
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QCompleter, QComboBox, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from database import mysqlDB
from main_UI import Ui_main_view

# ui conversion code
#pyuic5 -x "I:\School project(dms,sdoop)\library_database_management.ui" -o main_UI.py

"""
ToDo - create add and delete functions for table widgets
ToDo - create popup view for inputing books and users
"""
class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.main_win.setFixedSize(1000, 800)
        self.ui = Ui_main_view()
        self.ui.setupUi(self.main_win)
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

        self.sql = mysqlDB()

        self.cursor = self.sql.dbcursor

        # main_page_elements
        self.IssuePage()
        self.ReturnPage()
        self.BooksPage()
        self.UsersPage()
        self.BookStatusPage()

    def showUI(self):
        self.main_win.show()

    def IssuePage(self):
        self.LoadBooksData()
        self.LoadUsersData()
        self.ui.issue_button.clicked.connect(self.goto_issue_page)
        self.usercombo = self.ui.issue_user_comboBox
        self.bookcombo = self.ui.issue_book_comboBox

        self.ui.issue_back_button.clicked.connect(self.goto_mainPage_page)
        self.bookcombo.activated.connect(self.BookComboAction)
        self.usercombo.activated.connect(self.UserComboAction)
        self.BookComboBoxData()
        self.UsersComboBoxData()
        self.usercombo.addItems(self.users)
        self.bookcombo.addItems(self.books)
        
        self.bookcombo.setEditable(True)
        self.bookcombo.setDuplicatesEnabled(False)
        self.bookcombo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.bookcombo.setInsertPolicy(QComboBox.NoInsert)
        
        self.usercombo.setEditable(True)
        self.usercombo.setDuplicatesEnabled(False)
        self.usercombo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.usercombo.setInsertPolicy(QComboBox.NoInsert)
        
        self.ui.confirm_issue_pushButton.clicked.connect(self.ConfirmIssue)
        self.bookcombo.currentTextChanged.connect(self.BookComboAction)
        self.usercombo.currentTextChanged.connect(self.UserComboAction)
        self.ui.issue_dateEdit.setCalendarPopup(True)
        today = QDate().currentDate()
        self.ui.issue_dateEdit.setDate(today)
        self.ui.day_spinBox.textChanged.connect(self.SetReturnDate)
        retun = self.ui.issue_dateEdit.date().addDays(self.ui.day_spinBox.value()).toPyDate()
        self.ui.return_date_label.setText(str(retun.day)+"-"+str(retun.month)+"-"+str(retun.year))

    def ReturnPage(self):
        self.ui.return_button.clicked.connect(self.goto_return_page)
        self.ui.return_back_button.clicked.connect(self.goto_mainPage_page)

    def BooksPage(self):
        self.ui.book_button.clicked.connect(self.goto_book_page)
        self.ui.book_back_Button.clicked.connect(self.goto_mainPage_page)
        self.LoadBooksData()

    def UsersPage(self):
        self.ui.user_back_button.clicked.connect(self.goto_mainPage_page)
        self.ui.user_button.clicked.connect(self.goto_user_page)
        self.LoadUsersData()

    def BookStatusPage(self):
        self.ui.book_status_button.clicked.connect(self.goto_BookStatus_page)
        self.ui.book_status_back_button.clicked.connect(self.goto_mainPage_page)

    # User and book lists function
    def GetBookColumns(self):
        self.cursor.execute("SHOW COLUMNS FROM books")
        self.books_column_names = [x[0] for x in self.cursor.fetchall()]

    def GetBooksData(self):
        self.cursor.execute("select * from books")
        self.books_list = [x for x in self.cursor.fetchall()]

    def GetUserColumns(self):
        self.cursor.execute("SHOW COLUMNS FROM users")
        self.users_column_names = [x[0] for x in self.cursor.fetchall()]

    def GetUsersData(self):
        self.cursor.execute("select * from users")
        self.user_list = [x for x in self.cursor.fetchall()]

    def GetIssuedColumns(self):
        self.cursor.execute("SHOW COLUMNS FROM issued")
        self.books_column_names = [x[0] for x in self.cursor.fetchall()]

    def GetIssuedData(self):
        self.cursor.execute("select * from issued")
        self.issued_books = [x for x in self.cursor.fetchall()]

    def LoadBooksData(self):
        self.BookTable = self.ui.book_tableWidget
        self.GetBooksData()
        self.GetBookColumns()
        del self.books_column_names[3]
        self.books_column_names[1] = "Book Name"
        self.books_column_names[2] = "Author Name"

        self.BookTable.setRowCount(len(self.books_list))
        self.BookTable.setColumnCount(len(self.books_column_names))
        self.BookTable.setHorizontalHeaderLabels(self.books_column_names)

        header = self.BookTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        row = 0

        for book in self.books_list:
            self.BookTable.setItem(row,0,QtWidgets.QTableWidgetItem(str(book[0])))
            self.BookTable.setItem(row,1,QtWidgets.QTableWidgetItem(book[1]))
            self.BookTable.setItem(row,2,QtWidgets.QTableWidgetItem(book[2]+" "+book[3]))
            row += 1

    def LoadUsersData(self):
        self.UserTable = self.ui.user_tableWidget
        self.GetUserColumns()
        self.GetUsersData()

        del self.users_column_names[2]
        self.users_column_names[0] = "User ID"
        self.users_column_names[1] = "User Name"
        
        self.UserTable.setRowCount(len(self.user_list))
        self.UserTable.setColumnCount(len(self.users_column_names))
        self.UserTable.setHorizontalHeaderLabels(self.users_column_names)
        
        header = self.UserTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        
        row = 0
        
        for user in self.user_list:
            self.UserTable.setItem(row,0,QtWidgets.QTableWidgetItem(str(user[0])))
            self.UserTable.setItem(row,1,QtWidgets.QTableWidgetItem(user[1]+" "+user[2]))
            self.UserTable.setItem(row,2,QtWidgets.QTableWidgetItem(str(user[3])))
            row += 1

    # issue and return function
    def UserComboAction(self):
        self.GetUsersData()
        user_name_dict = dict([(str(x[0]), x[1] +" "+x[2]) for x in self.user_list])
        user = user_name_dict.get(self.ui.issue_user_comboBox.currentText())
        if user:
            self.ui.name_info_label.setText(user)
        else:
            self.ui.name_info_label.setText("Invalid input")

    def BookComboAction(self):
        self.GetBooksData()
        book_name_dict = dict([(str(x[0]), x[1]) for x in self.books_list])
        book = book_name_dict.get(self.ui.issue_book_comboBox.currentText())
        if book:
            self.ui.book_info_label.setText(book)
        else:
            self.ui.book_info_label.setText("Invalid input")

    def ConfirmIssue(self):
        bookID = self.bookcombo.currentText()
        userID = self.usercombo.currentText()
        issue = str(self.ui.issue_dateEdit.date().toPyDate())
        retun = str(self.ui.issue_dateEdit.date().addDays(self.ui.day_spinBox.value()).toPyDate())
        query =  "insert into issued values (%s,%s,%s,%s)"
        data = (bookID,userID,issue,retun)
        try:
            self.cursor.execute(query,data)
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
        retun = self.ui.issue_dateEdit.date().addDays(self.ui.day_spinBox.value()).toPyDate()
        self.ui.return_date_label.setText(str(retun.day)+"-"+str(retun.month)+"-"+str(retun.year))

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
            self.usercombo.addItems(self.users)
        if self.users != self.last_users:
            self.bookcombo.addItems(self.books)
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
    def goto_mainPage_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

    # Books list

#####################################xus

#####################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.showUI()
    sys.exit(app.exec_())