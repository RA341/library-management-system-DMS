import mysql.connector

"""
Database features

create views for books and users
create a function to calculate fine
"""


class mysqlDB:
    def ConnectToMysql(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="password"
            )

            self.dbcursor = self.db.cursor()
            print("Connected to MySql Successfully")

        except Exception as e:
            print("Error connecting to mySQL server")
            print(e)
            quit(-1)

    def ConnectToDatabase(self, dbname):
        try:
            self.dbcursor.execute("create database if not exists " + dbname)

            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="password",
                database="librarydb"
            )
            self.dbcursor = self.db.cursor()
            self.db.autocommit = True

            print("Connected to Database Successfully")

            return self.dbcursor

        except Exception as e:
            print("Error connecting to database")
            print(e)
            quit(-1)

    def CreateTables(self):
        self.dbcursor.execute("create table IF NOT EXISTS books(\
                ISBN BIGINT(13),\
                Book_Name varchar(30),\
                Author_FName varchar(30),\
                Author_LName varchar(30),\
                PRIMARY KEY (ISBN));")

        self.dbcursor.execute("create table IF NOT EXISTS users(\
                    UID int,\
                    FName varchar(30),\
                    LName varchar(30),\
                    phoneNo varchar(30),\
                    PRIMARY KEY (UID));")

        self.dbcursor.execute("create table IF NOT EXISTS issued(\
                    ISBN BIGINT(13),\
                    UID int,\
                    issue_date date,\
                    return_date date,\
                    PRIMARY KEY (ISBN),\
                    FOREIGN KEY (ISBN) REFERENCES books(ISBN) ON DELETE CASCADE,\
                    FOREIGN KEY (UID) REFERENCES users(UID) ON DELETE CASCADE);")

        print("Tables created Successfully")

    def CreateViews(self):
        self.dbcursor.execute(
            "create or replace VIEW getusers AS \
            SELECT UID,CONCAT(FName, ' ', LName) AS 'User Name',phoneNo as 'Phone No' FROM  users;")

        self.dbcursor.execute(
            "create or replace VIEW getbooks AS \
            SELECT ISBN,CONCAT(Author_FName, ' ', Author_LName) AS 'Author Name',Book_Name as 'Book Name' FROM  books;")

        self.dbcursor.execute(
            "create or replace VIEW getissued AS \
            SELECT ISBN,UID as 'User ID',issue_date as 'Issue Date',return_date as 'Return Date' FROM  issued;")

        print("Views Created Successfully")

    def __init__(self):
        self.ConnectToMysql()
        self.dbcursor = self.ConnectToDatabase("librarydb")
        self.CreateTables()
        self.CreateViews()


if __name__ == "__main__":
    r = mysqlDB()
