import sys
from PyQt5 import QtWidgets, QtSql
from PyQt5.Qt import Qt
from getpass import getpass
from mysql.connector import connect, Error
from PyQt5.QtWidgets import QDialog, QApplication
import menu, projects, config, customers, departments, employees, employee_add, project_add, customer_projects, customer_add, triggers_add
from datetime import datetime

class Main(QtWidgets.QMainWindow, menu.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()

    def init(self):
        #назначаем действия по кнопкам
        self.pushButton_9.clicked.connect(self.projectlist)
        self.pushButton_3.clicked.connect(self.customerlist)
        self.pushButton_2.clicked.connect(self.departmentlist)
        self.pushButton_4.clicked.connect(self.employeelist)
        self.pushButton_19.clicked.connect(self.employee_add)
        self.pushButton_20.clicked.connect(self.project_add)
        self.pushButton_17.clicked.connect(self.customerprojectlist)
        self.pushButton_21.clicked.connect(self.customer_add)
        self.pushButton_16.clicked.connect(self.trigger_add)
    
    def projectlist(self):
        self.projectlist = ProjectList()
        self.projectlist.show()
        self.hide()

    def customerlist(self):
        self.customerlist = CustomerList()
        self.customerlist.show()
        self.hide()

    def customerprojectlist(self):
        self.customerprojectlist = CustomerProjectList()
        self.customerprojectlist.show()
        self.hide()

    def departmentlist(self):
        self.departmentlist = DepartmentList()
        self.departmentlist.show()
        self.hide()

    def employeelist(self):
        self.employeelist = EmployeeList()
        self.employeelist.show()
        self.hide()

    def employee_add(self):
        self.employee_add = EmployeeAdd()
        self.employee_add.show()
        self.hide()

    def customer_add(self):
        self.customer_add = CustomerAdd()
        self.customer_add.show()
        self.hide()

    def project_add(self):
        self.project_add = ProjectAdd()
        self.project_add.show()
        self.hide()

    def trigger_add(self):
        self.trigger_add = TriggerCreator()
        self.trigger_add.create_trigger()


class ProjectList(QtWidgets.QMainWindow, projects.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
            ) as connection:
                select_query = "select * from project"
                with connection.cursor() as cursor:
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    self.tableWidget.setRowCount(len(result))
                    b = list()
                    for row in result:
                        for i in row:
                            b.append(i)

                    k = 0
                    for j in range(0, len(result)):
                        for i in range(0, 8):
                            self.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(b[k])))
                            k += 1
            
    def init(self):
        self.pushButton_4.clicked.connect(self.back)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

class CustomerList(QtWidgets.QMainWindow, customers.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
            ) as connection:
                select_query = "select * from customer"
                with connection.cursor() as cursor:
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    self.tableWidget.setRowCount(len(result))
                    b = list()
                    for row in result:
                        for i in row:
                            b.append(i)

                    k = 0
                    for j in range(0, len(result)):
                        for i in range(0, 4):
                            self.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(b[k])))
                            k += 1
                   
    def init(self):
        self.pushButton_4.clicked.connect(self.back)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

class DepartmentList(QtWidgets.QMainWindow, departments.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
            ) as connection:
                select_query = "select * from department"
                with connection.cursor() as cursor:
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    self.tableWidget.setRowCount(len(result))
                    b = list()
                    for row in result:
                        for i in row:
                            b.append(i)

                    k = 0
                    for j in range(0, len(result)):
                        for i in range(0, 4):
                            self.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(b[k])))
                            k += 1
                   
    def init(self):
        self.pushButton_4.clicked.connect(self.back)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

class CustomerProjectList(QtWidgets.QMainWindow, customer_projects.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
            ) as connection:
                select_query = "select * from customerview"
                with connection.cursor() as cursor:
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    self.tableWidget.setRowCount(len(result))
                    b = list()
                    for row in result:
                        for i in row:
                            b.append(i)

                    k = 0
                    for j in range(0, len(result)):
                        for i in range(0, 2):
                            self.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(b[k])))
                            k += 1
                   
    def init(self):
        self.pushButton_4.clicked.connect(self.back)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

class EmployeeList(QtWidgets.QMainWindow, employees.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
            ) as connection:
                select_query = "select * from employee"
                with connection.cursor() as cursor:
                    cursor.execute(select_query)
                    result = cursor.fetchall()
                    self.tableWidget.setRowCount(len(result))
                    b = list()
                    for row in result:
                        for i in row:
                            b.append(i)

                    k = 0
                    for j in range(0, len(result)):
                        for i in range(0, 6):
                            self.tableWidget.setItem(j, i, QtWidgets.QTableWidgetItem(str(b[k])))
                            k += 1
                   
    def init(self):
        self.pushButton_4.clicked.connect(self.back)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

class EmployeeAdd(QtWidgets.QMainWindow, employee_add.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
               
    def init(self):
        self.pushButton_4.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

    def delete(self):
        id = self.lineEdit_2.text()
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
        ) as connection:
            delete_query = "DELETE from employee where employeeID = %s"
            delete_tuple = [(id,)]
            with connection.cursor() as cursor:
                cursor.execute(delete_query, delete_tuple[0])
                connection.commit()
        
                self.lineEdit_2.setText("")

    def add(self):
        name = self.lineEdit.text()
        departmentID = self.lineEdit_3.text()
        position = self.lineEdit_4.text()
        salary = self.lineEdit_5.text()
        hire_date = self.lineEdit_6.text()
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
            ) as connection:
                insert_query = "INSERT INTO Employee (name, position, hire_date, salary, departmentID) VALUES (%s, %s, %s, %s, %s)"
                insert_tuple = [(name, position, hire_date, salary, departmentID)]
                with connection.cursor() as cursor:
                    cursor.execute(insert_query, insert_tuple[0])
                    connection.commit()
        
                    self.lineEdit.setText("")
                    self.lineEdit_3.setText("")
                    self.lineEdit_4.setText("")
                    self.lineEdit_5.setText("")
                    self.lineEdit_6.setText("")

class ProjectAdd(QtWidgets.QMainWindow, project_add.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
               
    def init(self):
        self.pushButton_4.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

    def delete(self):
        id = self.lineEdit_2.text()
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
        ) as connection:
            delete_query = "DELETE from project where projectID = %s"
            delete_tuple = [(id,)]
            with connection.cursor() as cursor:
                cursor.execute(delete_query, delete_tuple[0])
                connection.commit()
        
                self.lineEdit_2.setText("")

    def add(self):
        name = self.lineEdit.text()
        description = self.lineEdit_3.text()
        start_date = self.lineEdit_4.text()
        end_date = self.lineEdit_5.text()
        budget = self.lineEdit_6.text()
        customerID = self.lineEdit_7.text()
        employeeID = self.lineEdit_8.text()
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
            ) as connection:
                insert_query = "INSERT INTO Project (name, description, start_date, end_date, budget, customerID, employeeID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                insert_tuple = [(name, description, start_date, end_date, budget, customerID, employeeID)]
                with connection.cursor() as cursor:
                    cursor.execute(insert_query, insert_tuple[0])
                    connection.commit()
        
                    self.lineEdit.setText("")
                    self.lineEdit_3.setText("")
                    self.lineEdit_4.setText("")
                    self.lineEdit_5.setText("")
                    self.lineEdit_6.setText("")
                    self.lineEdit_7.setText("")
                    self.lineEdit_8.setText("")

class CustomerAdd(QtWidgets.QMainWindow, customer_add.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()
               
    def init(self):
        self.pushButton_4.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.add)

    def back(self):
        self.driver = Main()
        self.driver.show()
        self.hide()

    def add(self):
        customerID = self.lineEdit_5.text()
        name = self.lineEdit.text()
        phone_number= self.lineEdit_3.text()
        email = self.lineEdit_4.text()
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
        ) as connection:
            select_query = "call create_customer(%s, %s, %s, %s)"
            select_tuple = [(customerID, name, phone_number, email )]
            with connection.cursor() as cursor:
                cursor.execute(select_query, select_tuple[0])
                connection.commit()

                self.lineEdit_4.setText("")
                self.lineEdit_3.setText("")
                self.lineEdit.setText("")
                self.lineEdit_5.setText("")
      
class TriggerCreator:
        
    def create_trigger(self):
        with connect(
                host="localhost",
                user="root",
                password=config.password,
                database=config.database,
        ) as connection:
            query = triggers_add.EmployeeSalaryUpdateTrigger
            query1= triggers_add.EmployeeInsertTrigger
            with connection.cursor() as cursor:
                cursor.execute(query)
                cursor.execute(query1)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()

if __name__ == '__main__':
    main()
