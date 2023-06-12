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