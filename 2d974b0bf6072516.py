import mysql.connector
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QPushButton, QDesktopWidget, QWidget
from getpass import getpass
from mysql.connector import connect, Error

myDB='IT_Company'

DepartmentCreate="""
CREATE TABLE IF NOT EXISTS Department (
    departmentID  INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    manager VARCHAR(50) NOT NULL,
    number_of_employees INT NOT NULL
);
"""

CustomerCreate="""
CREATE TABLE IF NOT EXISTS Customer (
    customerID  INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,    
    phone_number VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL
);
"""

EmployeeCreate="""
CREATE TABLE IF NOT EXISTS Employee(
    employeeID  INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    departmentID INT NOT NULL,  
    position VARCHAR(50) NOT NULL,    
    salary INT NOT NULL,
    hire_date DATE NOT NULL,
    FOREIGN KEY (departmentID) REFERENCES Department (departmentID)  
);
""" 

ProjectCreate="""
CREATE TABLE IF NOT EXISTS Project (
    projectID  INT PRIMARY KEY AUTO_INCREMENT,    
    name VARCHAR(50) NOT NULL,
    description VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget INT NOT NULL,
    customerID INT NOT NULL,
    employeeID INT NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customer (customerID),
    FOREIGN KEY (employeeID) REFERENCES Employee (employeeID)
);
"""

# Внесение данных в таблицу
DepartmentInsertIT_Company = """
INSERT INTO Department (departmentID, name, manager, number_of_employees)
    VALUES ('1', 'Дизайнеры', 'Елена', '20'),
           ('2', 'Программисты', 'Ольга', '10'),
           ('3', 'Тестировщики', 'Андрей', '4'),
           ('4', 'Проджект менеджеры', 'Александр', '2');
"""
EmployeeInsertIT_Company = """
INSERT INTO Employee (employeeID, name, position, hire_date, salary, departmentID) 
    VALUES (1, 'Мария Петрова', 'gt', '2022-05-10', '20000', '2'),
          (2, 'Алина Алиновна', 'бб', '2023-05-10', '20000', '1')
"""

CustomerInsertIT_Company = """
INSERT INTO Customer (customerID,  name, phone_number, email)
    VALUES ('1', 'Kamisama Hajimemashita', '+7(123)456-78-90', 'alexandr@mail.ru' )      
"""

ProjectInsertIT_Company = """
INSERT INTO Project (projectID , name, description, start_date , end_date, budget,  customerID, employeeID)
    VALUES (1, 'Разработка сайта', 'Разработка мрмрмил','2022-05-10', '2023-05-10', '500000', '1', '2')  
 """

 
#Список сотрудников по департаментам: это представление может помочь узнать, сколько сотрудников работает в каждом департаменте и кто является их менеджером
CREATEPROCEDURE1=""" 
CREATE PROCEDURE EmployeeListByDepartment()
BEGIN
    SELECT 
        d.name AS department_name,
        d.manager AS department_manager,
        e.name AS employee_name,
        e.position AS employee_position
    FROM Department d
    INNER JOIN Employee e ON d.departmentID = e.departmentID
    ORDER BY d.departmentID, e.employeeID;
END; 
"""
CREATEPROCEDURE2="""
CREATE PROCEDURE create_customer(IN customerID INT, IN name VARCHAR(50), IN phone_number VARCHAR(50), IN email VARCHAR(50))
BEGIN
  INSERT INTO Customer (customerID, name, phone_number, email)
  VALUES (customerID, name, phone_number, email);
END  
""" 


# Trigger 1: Удаление отдела
DepartmentDeleteTrigger = """
CREATE TRIGGER delete_dependent_employee
BEFORE DELETE ON Department
FOR EACH ROW
BEGIN
    DELETE FROM Employee WHERE departmentID = OLD.departmentID;
END;
"""

# Trigger 2: Обновление бюджета проекта при изменении зарплаты сотрудника
EmployeeSalaryUpdateTrigger = """
CREATE TRIGGER update_project_budget
AFTER UPDATE ON Employee
FOR EACH ROW
BEGIN
    UPDATE Project SET budget = (budget + NEW.salary - OLD.salary) WHERE employeeID = NEW.employeeID;
END;
"""

# Trigger 3: Обновление количества сотрудников в отделе при добавлении нового сотрудника
EmployeeInsertTrigger = """
CREATE TRIGGER update_department_employee_count
AFTER INSERT ON Employee
FOR EACH ROW
BEGIN
    UPDATE Department SET number_of_employees = (number_of_employees + 1) WHERE departmentID = NEW.departmentID;
END;
"""

#представление, которое  отображает идентификатор клиента и список его проектов
CustomerView="""
CREATE VIEW CustomerView AS
SELECT customerID, GROUP_CONCAT(name SEPARATOR ', ') AS projects
FROM Project
WHERE customerID IS NOT NULL
GROUP BY customerID
"""

#представление, которое  отображает информацию о сотрудниках и названии их департамента
EmployeeView="""
CREATE VIEW EmployeeView AS
SELECT employeeID, name, Department.name AS department, position, salary, hire_date
FROM Employee
JOIN Department ON Employee.departmentID = Department.departmentID
"""

TransactionCreate="""
START TRANSACTION;

-- Добавление нового отдела
INSERT INTO Department (name, manager, number_of_employees)
VALUES ('Marketing', 'Anna Smith', 10);

-- Добавление нового клиента
INSERT INTO Customer (name, phone_number, email)
VALUES ('John Doe', '1234567890', 'johndoe@example.com');

-- Добавление нового сотрудника
INSERT INTO Employee (name, departmentID, position, salary, hire_date)
VALUES ('Sarah Johnson', 1, 'Marketing Manager', 5000, '2022-01-01');

-- Добавление нового проекта и назначение его клиенту и сотруднику
INSERT INTO Project (name, description, start_date, end_date, budget, customerID, employeeID)
VALUES ('Marketing Campaign', 'New product launch campaign', '2022-01-15', '2022-03-15', 10000, 1, 1);

-- Проверка выполнения операций
IF @@ROWCOUNT = 4
    COMMIT;
ELSE
    ROLLBACK;
"""




while True: # организуем циклическое выполнение задач
    print ("""меню:  1 - ПОДКЛЮЧЕНИЕ, #####2 - ПЕРЕЗАЛИВКА, 3 - ЗАПРОС ВЫБОРКИ,
       4 - ВЫВОД ВСЕХ ДАННЫХ ИЗ ТАБЛИЦЫ ОТДЕЛЫ, 5 - ВЫВОД ДАННЫХ ИЗ ТАБЛИЦЫ РАБОТНИКИ, 6 - ВЫВОД ДАННЫХ ИЗ ТАБЛИЦЫ ЗАКАЗЧИКИ, 7 - ВЫВОД ДАННЫХ ИЗ ТАБЛИЦЫ ПРОЕКТЫ,
       8 - ВВОД ДАННЫХ В ТАБЛИЦУ РАБОТНИКИ, 9 - ВВОД ДАННЫХ В ТАБЛИЦУ ПРОЕКТЫ, 10 - ВВОД ДАННЫХ В ТАБЛИЦУ ЗАКАЗЧИКИ,  11 - ВВОД ДАННЫХ В ТАБЛИЦУ КЛИЕНТЫ,
       12 - ЗАПРОС НА ВЫБОРКУ РАБОТНИКА ПО ОТДЕЛУ, 13- ЗАПРОС НА ВЫБОРКУ ДАТЫ ОКНОЧАНИЯ ПРОЕКТА, 14 -ВЫЗОВ ПРОЦЕДУРЫ, 15 - ПЕРЕЗАЛИВКА ПРОЦЕДУР, 16- ПЕРЕЗАЛИВКА ТРИГГЕРОВ, 
        17 - ВЫЗОВ ВТОРОЙ ПРОЦЕДУРЫ, 18 - ВЫВОД ПРЕДСТАВЛЕНИЯ 1, 19 - ВЫВОД ПРЕДСТАВЛЕНИЯ 2, 0 - ВЫХОД""")
    Code = int(input('Ваш выбор '))
    
    if Code==0 : # завершаем сеанс работы с БД
        try:
            cnx.close()
            print ('сеанс работы с БД завершен')
        except mysql.connector.Error as err:
            print (err)
        finally:
            break      
       
    elif Code==1: # подключаемся к БД и создаем курсор
        try:
            cnx = mysql.connector.connect(user='root', password = '89181024524Ni@', database = myDB)
            cursor1= cnx.cursor()
            print ('подключение к БД выполнено')
        except mysql.connector.Error as err:
            print (err)
    
    elif Code==2:
        try:
            cursor1.execute("DROP TABLE IF EXISTS Project")
            print ('таблица Project удалена') 
        except mysql.connector.Error as err:
            print (err)
        try:
            cursor1.execute("DROP TABLE IF EXISTS Employee")
            print ('таблица Employee удалена')
        except mysql.connector.Error as err:
            print (err)
        try:
            cursor1.execute("DROP TABLE Customer")
            print ('таблица Customer удалена') 
        except mysql.connector.Error as err:
            print (err)    
        
        try:
            cursor1.execute("DROP TABLE IF EXISTS Department")
            print ('таблица Department удалена') 
        except mysql.connector.Error as err:
            print (err)

        # создаем таблицы (важен порядок!)
        try:
            cursor1.execute(DepartmentCreate)
            print ('таблица Department создана') 
        except mysql.connector.Error as err:
            print (err)
        
        try:
            cursor1.execute(EmployeeCreate)
            print ('таблица Employee создана') 
        except mysql.connector.Error as err:
            print (err)        

        try:
            cursor1.execute(CustomerCreate)
            print ('таблица Customer создана') 
        except mysql.connector.Error as err:
            print (err)        
        try:
            cursor1.execute(ProjectCreate)
            print ('таблица Project создана') 
        except mysql.connector.Error as err:
            print (err)
                    
 # вставляем тестовые данные
        try:
            cursor1.execute(DepartmentInsertIT_Company)
            cnx.commit() 
            print ('данные о Department введены')
        except mysql.connector.Error as err:
            print (err)
        try:
            cursor1.execute(EmployeeInsertIT_Company)
            cnx.commit() 
            print ('данные о Employee введены')
        except mysql.connector.Error as err:
            print (err)
            
        try:
            cursor1.execute(CustomerInsertIT_Company)
            cnx.commit() 
            print ('данные о Customer введены')
        except mysql.connector.Error as err:
            print (err)            
            
        try:
            cursor1.execute(ProjectInsertIT_Company)
            cnx.commit() 
            print ('данные о Project введены')
        except mysql.connector.Error as err:
            print (err)            
             
       
            
    elif Code==3: # выполняем произвольный запрос на выборку данных
        Query1 = input ('Введите запрос на выборку данных:')
        try: 
            cnx.start_transaction()
            cursor1.execute(Query1)
            for row in cursor1.fetchall():
                print (row)
                cnx.commit()
        except mysql.connector.Error as err:
            print (err)
            

    elif Code==4: # выполняем запрос на выборку данных Department
            QueryB="SELECT * FROM Department"
            try: #вывод таблицы Department
                cursor1.execute(QueryB) 
                for (departmentID, name, manager, number_of_employees) in cursor1:
                      print ('ID.department: {}. Отдел: {}. Руководитель отдела: {}.Число сотрудников: {}'.format(departmentID, name, manager, number_of_employees))
            except mysql.connector.Error as err:
                print (err)

    elif Code==5:
        QueryC="SELECT Employee.employeeID, Employee.name, Employee.position, Employee.hire_date, Employee.salary, Department.name FROM Employee INNER JOIN Department ON Employee.departmentID = Department.departmentID"
        try:
            cursor1.execute(QueryC)
            for (employeeID, name, position, hire_date, salary, department_name) in cursor1:
                print ('ID сотрудника: {}. Имя: {}. Должность: {}. Дата приема на работу: {}. Зарплата: {}. Отдел: {}'.format(employeeID, name, position, hire_date, salary, department_name))
        except mysql.connector.Error as err:
            print (err)


    elif Code==6: 
        QueryV="SELECT * FROM Customer"
        try: 
            cursor1.execute(QueryV) 
            for (customerID,  name,phone_number, email) in cursor1:
                print ('ID.customer: {}. ФИО: {}. Номер телефона: {}. Email: {}'.format(customerID,  name, phone_number, email))
        except mysql.connector.Error as err:
            print (err)

    elif Code==7: 
        QueryV="SELECT Project.projectID, Project.name, Project.description, Project.start_date, Project.end_date, Project.budget, Customer.name, Employee.name FROM Project JOIN Customer ON Project.customerID = Customer.customerID JOIN Employee ON Project.employeeID = Employee.employeeID"
        try: 
            cursor1.execute(QueryV) 
            for (projectID, name, description, start_date, end_date, budget, customer_name, employee_name) in cursor1:
                print ('ID проекта: {}. Название проекта: {}. Описание: {}. Дата начала: {}. Дата конца: {}. Бюджет: {}. Заказчик: {}. Csотрудник: {}'.format(projectID, name, description, start_date, end_date, budget, customer_name, employee_name))
        except mysql.connector.Error as err:
            print (err)

    elif Code==8: 
        print ('Введите данные о работнике')
        employeeID = input("Введите ID работника: ")
        name = input("Введите ФИО: ")
        departmentID= input("Ведите номер отдела: ")  
        position =  input("Введите должность: ")    
        salary = input("Введите зарплату: ") 
        hire_date = input("Введите дату приема на работу в формате ГГГГ-ММ-ДД:: ") 
        QueryInputEmployee = """INSERT INTO Employee (employeeID, name, position, hire_date, salary, departmentID) 
        VALUE ('{}','{}','{}','{}','{}','{}')""".format (employeeID, name, position, hire_date, salary, departmentID)
        values = (employeeID, name, position, hire_date, salary, departmentID)
        print (QueryInputEmployee)
        try: 
            cursor1.execute(QueryInputEmployee)
            print ('данные введены')
        except mysql.connector.Error as err:
            print (err)

    elif Code==9: 
        print ('Введите данные о проекте')
        #projectID = input("Введите ID проекта: ")        
        name = input("Введите название проекта: ")
        description = input("Введите описание проекта: ") 
        start_date  = input("Введите дату начала проекта в формате ГГГГ-ММ-ДД: ") 
        end_date = input("Введите дату окончания проекта в формате ГГГГ-ММ-ДД: ")
        budget = input("Введите бюджет проекта: ")
        customerID = input("Введите ID заказчика: ")
        employeeID = input("Введите ID сотрудника: ") 
        QueryInputProject = """INSERT INTO Project (name, description, start_date, end_date, budget, customerID, employeeID) 
        VALUE ('{}','{}','{}','{}','{}','{}','{}')""".format ( name, description, start_date, end_date, budget, customerID, employeeID)
        values = ( name, description, start_date, end_date, budget, customerID, employeeID)#projectID,
        print (QueryInputProject)
        try: 
            cursor1.execute(QueryInputProject)
            print ('данные введены')
        except mysql.connector.Error as err:
            print (err)

 




    elif Code == 14:
        # Вызываем процедуру EmployeeListByDepartment()
        try:
            cursor1.callproc("EmployeeListByDepartment")
            # Получаем результаты
            results = cursor1.fetchall()
            for row in results:
                print(row)
        except mysql.connector.Error as err:
            print(err)          
        
print ('работа программы завершена')


