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
);"""