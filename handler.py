from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox
import sys

class DataBase:
    def __init__(self):
        super(DataBase, self).__init__()
        self.connect()


    def connect(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName("GAME_CLUB_db.db")

        if not db.open():
            # QtWidgets.QMessageBox.critical(None, "Cannot open database",
            #                                 "Click Cancel to exit.", QtWidgets.QMessageBox.Cancel)
            return False

        query = QSqlQuery()
        query.exec("""CREATE TABLE IF NOT EXISTS пользователи (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      админ TEXT DEFAULT no,
                      логин TEXT,
                      пароль TEXT,
                      имя TEXT,
                      фамилия TEXT,
                      номер_телефона TEXT
                      )""")

        query.exec("""CREATE TABLE IF NOT EXISTS игровая_сессия (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                      id_пользователь INTEGER REFERENCES пользователи(id),
                                      номер_места TEXT,
                                      дата TEXT,
                                      время TEXT,
                                      цена REAL)""")

#        query.exec("""CREATE VIEW IF NOT EXISTS vi as select логин, пароль from пользователи where логин a""")

        return True


    def execute(self, sql_query, query_values=None):
        query = QSqlQuery()
        query.prepare(sql_query)

        if query_values is not None:
            for query_value in query_values:
                query.addBindValue(query_value)

        query.exec()
        return query

    def admin_user(self, login, password):
        query = QSqlQuery()
        query.prepare("SELECT * FROM пользователи WHERE логин = ? AND пароль = ?")
        query.bindValue(0, login)
        query.bindValue(1, password)
        if query.exec() and query.next():
            return query.record()
        else:
            return None

    def user_job(self,name, lastname, number, id):
        sql_query = "UPDATE пользователи SET имя=?, фамилия=?, номер_телефона=? WHERE ID=?"
        self.execute(sql_query, [name, lastname, number, id])

    def session_job(self, id, mesto, date, time):
        sql_query = "INSERT INTO игровая_сессия (id_пользователь, номер_места, дата, время) VALUES (?, ?, ?, ?)"
        self.execute(sql_query, [id, mesto, date, time])

    def add_user(self, login, password):
        sql_query = "INSERT INTO пользователи (логин, пароль) VALUES (?, ?)"
        self.execute(sql_query, [login, password])

    def new1(self, admin, login, password, name, lastname, number):
        sql_query = "INSERT INTO пользователи (админ, логин, пароль, имя, фамилия, номер_телефона) VALUES (?, ?, ?, ?, ?, ?)"
        self.execute(sql_query, [admin, login, password, name, lastname, number])


    def modify1(self, admin, login, password, name, lastname, number, id):
        sql_query = "UPDATE пользователи SET админ=?, логин=?, пароль=?, имя=?, фамилия=?, номер_телефона=? WHERE ID=?"
        self.execute(sql_query, [admin, login, password, name, lastname, number, id])

    def del1(self, id):
        sql_query = "DELETE FROM пользователи WHERE id=?"
        self.execute(sql_query, [id])

    def new2(self, id_user, mesto, date, time, price):
        sql_query = "INSERT INTO игровая_сессия (id_пользователь, номер_места, дата, время, цена) VALUES (?, ?, ?, ?, ?)"
        self.execute(sql_query, [id_user, mesto, date, time, price])


    def modify2(self, id_user, mesto, date, time, price, id):
        sql_query = "UPDATE игровая_сессия SET id_пользователь=?, номер_места=?, дата=?, время=?, цена=? WHERE ID=?"
        self.execute(sql_query, [id_user, mesto, date, time, price, id])

    def del2(self, id):
        sql_query = "DELETE FROM игровая_сессия WHERE id=?"
        self.execute(sql_query, [id])

    def select_on_date(self, date):
        query = QSqlQuery()
        query.prepare("SELECT id, имя, фамилия, номер_телефона FROM пользователи JOIN игровая_сессия ON пользователи.id = игровая_сессия.id_пользователь WHERE игровая_сессия.дата = :date")
        query.bindValue(":date", date)


        if not query.exec():
            print("Ошибка выполнения запроса:", query.lastError().text())
            sys.exit(1)

        x = query

        return x