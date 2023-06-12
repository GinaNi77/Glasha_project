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