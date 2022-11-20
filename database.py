import mysql.connector


class MySqlDB:
    def connectToMysql(self):
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

    def connectToDatabase(self):
        try:
            self.dbcursor.execute("create database if not exists " + self.dbname)

            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="password",
                database=self.dbname
            )
            self.dbcursor = self.db.cursor()
            self.db.autocommit = True

            print("Connected to Database Successfully")

            return self.dbcursor

        except Exception as e:
            print("Error connecting to database")
            print(e)
            quit(-1)

    def createTables(self):
        try:
            self.dbcursor.execute("create table IF NOT EXISTS books(\
                    ISBN BIGINT(13),\
                    Book_Name varchar(255),\
                    Author_FName varchar(30),\
                    Author_LName varchar(30),\
                    PRIMARY KEY (ISBN));")

            self.dbcursor.execute("create table IF NOT EXISTS users(\
                        UID BIGINT(10),\
                        FName varchar(30),\
                        LName varchar(30),\
                        phoneNo varchar(30),\
                        PRIMARY KEY (UID));")

            self.dbcursor.execute("create table IF NOT EXISTS issued(\
                        ISBN BIGINT(13),\
                        UID BIGINT(10),\
                        issue_date date,\
                        return_date date,\
                        PRIMARY KEY (ISBN),\
                        FOREIGN KEY (ISBN) REFERENCES books(ISBN) ON DELETE CASCADE,\
                        FOREIGN KEY (UID) REFERENCES users(UID) ON DELETE CASCADE);")

            print("Tables created Successfully")
        except Exception as table:
            print("Error creating tables")
            print(table)
            quit(-1)

    def createViews(self):
        try:
            self.dbcursor.execute(
                "create or replace VIEW getusers AS \
                SELECT  UID,\
                        CONCAT(FName, ' ', LName) AS 'User Name',\
                        phoneNo as 'Phone No'\
                FROM  users;")

            self.dbcursor.execute(
                "create or replace VIEW getbooks AS \
                SELECT  ISBN,\
                        CONCAT(Author_FName, ' ', Author_LName) AS 'Author Name',\
                        Book_Name as 'Book Name'\
                FROM  books;")

            self.dbcursor.execute(
                "create or replace VIEW getissued AS \
                SELECT  ISBN,\
                        UID as 'User ID',\
                        issue_date as 'Issue Date',\
                        return_date as 'Return Date',\
                        days(return_date) as 'Days Late',\
                        calculate_fines(days(return_date),100) as 'Total Fine'\
                        FROM  issued;")

            print("Views Created Successfully")

        except Exception as views:
            print("Error creating views")
            print(views)
            quit(-1)

    def createFunctions(self):
        try:
            self.dbcursor.execute("CREATE FUNCTION IF NOT EXISTS\
                            days(issue date) RETURNS int DETERMINISTIC\
                               BEGIN DECLARE currentdate DATE;\
                                Select current_date() into currentdate;\
                                   IF (currentdate > issue) THEN\
                                        RETURN datediff(currentdate,issue);\
                                   ELSE\
                                        RETURN 0;\
                                   END IF;\
                               END")

            self.dbcursor.execute("\
                CREATE FUNCTION IF NOT EXISTS\
                 calculate_fines(days int, rate int) RETURNS int DETERMINISTIC\
                    BEGIN\
                        RETURN days*rate;\
                    END")

            print("Functions Created Successfully")
        except Exception as func:
            print("Error creating functions")
            print(func)
            quit(-1)

    def createStoredProcedures(self):
        try:
            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                    getbookcolumnlist()\
                                     BEGIN\
                                        show columns from getbooks;\
                                     END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                    getbooklist()\
                                        BEGIN\
                                         select * from getbooks;\
                                        END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                            getusercolumnlist()\
                                             BEGIN\
                                                show columns from getusers;\
                                             END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                            getuserlist()\
                                             BEGIN\
                                                select * from getusers;\
                                             END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                            getissuedcolumnlist()\
                                             BEGIN\
                                                show columns from getissued;\
                                             END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                            getissuedlist()\
                                             BEGIN\
                                                select * from getissued;\
                                             END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                                        getnonissuedbooklist() \
                                                         BEGIN\
                                                            select * from getbooks where ISBN not in \
                                                            (select ISBN from getissued);\
                                                         END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                    delbooks (in bookid bigint)\
                                     BEGIN\
                                      delete from books where ISBN = bookid;\
                                     END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                    deluser (in userid bigint)\
                                     BEGIN\
                                        delete from users where UID = userid;\
                                     END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                    delissued (in bookid bigint)\
                                        BEGIN\
                                            delete from issued where ISBN = bookid;\
                                        END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                    addissuebook (in bookID bigint, in userID bigint, in issuedate date, in returndate date)\
                                        BEGIN\
                                            insert into issued values (bookID, userID, issuedate, returndate);\
                                        END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                     adduser (in uid bigint, in fname varchar(30), in lname varchar(30), in phone varchar(30))\
                                        BEGIN\
                                            insert into users values (uid, fname, lname, phone);\
                                        END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                     addbook (in bid bigint, in book_name varchar(255), in fname varchar(30), in lname varchar(30))\
                                        BEGIN\
                                            insert into books values (bid, book_name, fname, lname);\
                                        END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                                 updateuser (in uid bigint, in fname varchar(30), in lname varchar(30), in phone varchar(30))\
                                                    BEGIN\
                                                        update users set FName=fname, LName=lname, phoneNo=phone\
                                                        where UID = uid;\
                                                    END")

            self.dbcursor.execute("CREATE PROCEDURE IF NOT EXISTS\
                                                 updatebook (in bid bigint, in book_name varchar(255), in fname varchar(30), in lname varchar(30))\
                                                    BEGIN\
                                                        update books set Book_Name=book_name, Author_FName=fname, Author_LName=lname\
                                                        where ISBN = bid;\
                                                    END")

            print("Stored Procedures created Successfully")
        except Exception as storedprocedure:
            print("Error Creating stored procedures")
            print(storedprocedure)
            quit(-1)

    def __init__(self, dbname):
        try:
            self.dbname = dbname
            self.connectToMysql()
            self.dbcursor = self.connectToDatabase()
            self.createFunctions()
            self.createTables()
            self.createViews()
            self.createStoredProcedures()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    try:
        r = MySqlDB('librarydb')
    except Exception as e:
        print(e)
