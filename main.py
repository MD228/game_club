from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
import sys
from PyQt6.QtSql import QSqlTableModel
from Admin_interface import Ui_Admin_interface
from Registration import Ui_Registration
from Authorization import Ui_Authorization
from User_interface import Ui_User_interface
from UserDialog import Ui_User_Dialog
from SassionDialog import Ui_Session_Dialog
from handler import DataBase
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt6.QtWidgets import QTableView

class Main(QMainWindow):
    def __init__(self):
        super().__init__()


        #окно регистрации
        self.registration = QMainWindow()
        self.ui_registration = Ui_Registration()
        self.ui_registration.setupUi(self.registration)

        self.ui_registration.pushButton_Enter.clicked.connect(self.rega)

        #окно авторизации
        self.authorization = QMainWindow()
        self.ui_authorization = Ui_Authorization()
        self.ui_authorization.setupUi(self.authorization)

        #окно пользователя
        self.user = QMainWindow()
        self.ui_user = Ui_User_interface()
        self.ui_user.setupUi(self.user)

        self.ui_user.pushButton_2.clicked.connect(self.user_work)

        #окно администратора
        self.admin = QMainWindow()
        self.ui_admin = Ui_Admin_interface()
        self.ui_admin.setupUi(self.admin)
        self.db = DataBase()
        self.show_data1()
        self.show_data2()

        self.ui_admin.changeButton1.clicked.connect(self.user_dialogs)
        self.ui_admin.addButton1.clicked.connect(self.user_dialogs)
        self.ui_admin.deleteButton1.clicked.connect(self.deleter)

        self.ui_admin.changeButton2.clicked.connect(self.s_dialogs)
        self.ui_admin.addButton2.clicked.connect(self.s_dialogs)
        self.ui_admin.deleteButton2.clicked.connect(self.s_dialogs)

        self.ui_admin.pushButton.clicked.connect(self.select)

        #кнопки перемещения между окнами
        self.ui_registration.Btn_Authorization.clicked.connect(self.open_authorization_reg)
        self.ui_user.homeButton.clicked.connect(self.open_authorization_user)
        self.ui_admin.homeButton.clicked.connect(self.open_authorization_admin)
        self.ui_authorization.Btn_Registration.clicked.connect(self.open_registration_auth)
        self.ui_authorization.pushButton_Enter.clicked.connect(self.authorization_user)

    def show_data1(self):
        self.model = QSqlTableModel(self)
        self.model.setTable("пользователи")
        self.model.select()
        self.ui_admin.tableView1.setModel(self.model)

    def show_data2(self):
        self.model = QSqlTableModel(self)
        self.model.setTable("игровая_сессия")
        self.model.select()
        self.ui_admin.tableView2.setModel(self.model)

    def open_authorization_reg(self):
        self.registration.close()
        self.authorization.show()

    def open_authorization_user(self):
        self.user.close()
        self.authorization.show()

    def open_authorization_admin(self):
        self.admin.close()
        self.authorization.show()

    def open_registration_auth(self):
        self.authorization.close()
        self.registration.show()



    def authorization_user(self):
        login = self.ui_authorization.lineEdit_Login.text()
        password = self.ui_authorization.lineEdit_Password.text()
        admin = self.db.admin_user(login, password)
        self.ui_user.label.setText(admin.value(4))
        self.ui_user.label_2.setText(admin.value(5))
        self.ui_user.label_3.setText(admin.value(6))
        if admin:
            role = admin.value(1)

            if role == 'yes':
                self.admin.show()
                self.authorization.close()
            elif role == 'no':
                self.user.show()
                self.authorization.close()
        return admin.value(0)

    def user_work(self):
        id = self.authorization_user()
        name = self.ui_user.Name.toPlainText()
        lastname = self.ui_user.Lastname.toPlainText()
        number = self.ui_user.Phone_Number.toPlainText()
        mesto = self.ui_user.comboNumber.currentText()
        date = self.ui_user.dateEdit.text()
        time = self.ui_user.timeEdit.text()
        self.db.user_job(name, lastname, number, id)
        self.db.session_job(id, mesto, date, time)
        self.show_data1()
        self.show_data2()

    def rega(self):
        login = self.ui_registration.lineEdit_Login.text()
        password = self.ui_registration.lineEdit_Password.text()
        if not login or not password:
            return
        user = self.db.admin_user(login, password)
        if user:
            return
        self.db.add_user(login, password)
        self.authorization.show()
        self.registration.close()

    def user_dialogs(self):
        self.dialog_u = QDialog()
        self.ui_dialog_u = Ui_User_Dialog()
        self.ui_dialog_u.setupUi(self.dialog_u)
        self.dialog_u.show()
        sender = self.sender()
        if sender.text() == "a":
            self.ui_dialog_u.pushButton_Enter.clicked.connect(self.adder)
        else:
            self.ui_dialog_u.pushButton_Enter.clicked.connect(self.modifyer)

    def adder(self):
        admin = self.ui_dialog_u.lineEdit1.text()
        login = self.ui_dialog_u.lineEdit2.text()
        password = self.ui_dialog_u.lineEdit3.text()
        name = self.ui_dialog_u.lineEdit5.text()
        lastname = self.ui_dialog_u.lineEdit4.text()
        number = self.ui_dialog_u.lineEdit6.text()

        self.db.new1(admin, login, password, name, lastname, number)
        self.show_data1()
        self.dialog_u.close()

    def modifyer(self):
        index = self.ui_admin.tableView1.selectedIndexes()[0]
        id = str(self.ui_admin.tableView1.model().data(index))
        admin = self.ui_dialog_u.lineEdit1.text()
        login = self.ui_dialog_u.lineEdit2.text()
        password = self.ui_dialog_u.lineEdit3.text()
        name = self.ui_dialog_u.lineEdit5.text()
        lastname = self.ui_dialog_u.lineEdit4.text()
        number = self.ui_dialog_u.lineEdit6.text()

        self.db.modify1(admin, login, password, name, lastname, number, id)
        self.show_data1()
        self.dialog_u.close()

    def deleter(self):
        index = self.ui_admin.tableView1.selectedIndexes()[0]
        id = str(self.ui_admin.tableView1.model().data(index))
        self.db.del1(id)
        self.show_data1()

    def s_dialogs(self):
        self.dialog_s = QDialog()
        self.ui_dialog_s = Ui_Session_Dialog()
        self.ui_dialog_s.setupUi(self.dialog_s)
        self.dialog_s.show()
        sender = self.sender()
        if sender.text() == "a":
            self.ui_dialog_s.pushButton_Enter.clicked.connect(self.adder2)
        else:
            self.ui_dialog_s.pushButton_Enter.clicked.connect(self.modifyer2)

    def adder2(self):
        id_user = int(self.ui_dialog_s.lineEdit1.text())
        mesto = self.ui_dialog_s.lineEdit2.text()
        date = self.ui_dialog_s.lineEdit3.text()
        time = self.ui_dialog_s.lineEdit5.text()
        price = float(self.ui_dialog_s.lineEdit4.text())

        self.db.new2(id_user, mesto, date, time, price)
        self.show_data2()
        self.dialog_s.close()

    def modifyer2(self):
        index = self.ui_admin.tableView2.selectedIndexes()[0]
        id = str(self.ui_admin.tableView2.model().data(index))
        id_user = self.ui_dialog_s.lineEdit1.text()
        mesto = self.ui_dialog_s.lineEdit2.text()
        date = self.ui_dialog_s.lineEdit3.text()
        time = self.ui_dialog_s.lineEdit5.text()
        price = self.ui_dialog_s.lineEdit4.text()

        self.db.modify2(id_user, mesto, date, time, price, id)
        self.show_data2()
        self.dialog_s.close()

    def deleter2(self):
        index = self.ui_admin.tableView2.selectedIndexes()[0]
        id = str(self.ui_admin.tableView2.model().data(index))
        self.db.del2(id)
        self.show_data2()

    def select(self):
        model = QSqlQueryModel()
        date = str(self.ui_admin.dateEdit.text())
        x = self.db.select_on_date(date)
        model.setQuery(x)
        self.ui_admin.tableView_Info.setModel(model)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.authorization.show()
    sys.exit(app.exec())