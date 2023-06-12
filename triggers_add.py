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