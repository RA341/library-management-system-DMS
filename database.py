import mysql.connector


class MySqlDB:
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

    def CreateViews(self):
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

    def CreateFunctions(self):
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

    def CreateStoredProcedures(self):
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
                                delbooks (in bookid bigint)\
	                             BEGIN\
                                  delete from book where ISBN = bookid;\
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
                                 addbook (in bid bigint, in book_name varchar(30), in fname varchar(30), in lname varchar(30))\
                                	BEGIN\
                                        insert into books values (bid, book_name, fname, lname);\
                                	END")
        print("Stored Procedures created Successfully")

    def __init__(self):
        try:
            self.ConnectToMysql()
            self.dbcursor = self.ConnectToDatabase("librarydb")
            self.CreateFunctions()
            self.CreateTables()
            self.CreateViews()
            self.CreateStoredProcedures()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # r = MySqlDB()
    try:
        pass
    except Exception as e:
        print(e)
