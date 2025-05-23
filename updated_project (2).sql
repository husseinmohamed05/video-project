create database LAB;
use  LAB ;

create table if not exists laboratorian(
	laboratorianID varchar (8) primary key,
	firstName  text,
	middlename text,
    lastname text,
    phone Varchar (13),
	address text
);

insert into laboratorian (laboratorianID) VALUES
('L001'),
('L002'),
('L003'),
('L004'),
('L005'),
('L006');

create table patient(
	patientID varchar (9) primary key,
	firstname text,
	middlename text,
    lastname text,
    phone varchar (13),
	city text ,
	street text,
	country text,
	birthdate date,
	job text
);
INSERT INTO patient (patientID) VALUES
('P001'),
('P002'),
('P003'),
('P004'),
('P005'),
('P006'),
('P007'),
('P008'),
('P009'),
('P010'),
('P011'),
('P012');


create table medicalTest(
	testID varchar (9) primary key,
	name text,
	price int
);

insert into medicalTest (testID, name, price) values
('T001','CBC', 500),
('T002', 'AB', 400),
('T003','DIL', 300);

create table testResult(
	resultID varchar (9) primary key,
    testID varchar (9),
    patientID varchar (9),
    laboratorianID varchar (8),
	foreign key (testID) references medicalTest(testID) ,
	foreign key (patientID) references patient(patientID),
	foreign key (laboratorianID) references laboratorian(laboratorianID),
	testDate date,
	result text
);

INSERT INTO testResult (resultID) VALUES
('R001'),
('R002'),
('R003'),
('R004'),
('R005'),
('R006'),
('R007');

create table component(
	componentID varchar (9) PRIMARY KEY ,
	componentname text,
	availabeQuantity int ,
	MinQuantity int
);
INSERT INTO component (componentID,componentname) values
('C001','serum'),
('C002','A.B'),
('C003','Anistetic');

-- Table for many-to-many relationship between MedicalTest and Component
CREATE TABLE MedicalTest_component (
    testID VARCHAR(9),
    componentID VARCHAR(9),
    quantityUsed INT,
    PRIMARY KEY (testID, componentID),
    FOREIGN KEY (testID) REFERENCES medicalTest(testID),
    FOREIGN KEY (componentID) REFERENCES component(componentID)
);

-- Sample data for MedicalTest_Component
INSERT INTO MedicalTest_component (testID, componentID, quantityUsed) VALUES 
('T001', 'C001', 2),
('T001', 'C002', 1),
('T002', 'C001', 1),
('T003', 'C003', 3);

-- Table for relationship between Patient and Component (Takes)
CREATE TABLE Patient_component (
    patientID VARCHAR(9),
    componentID VARCHAR(9),
    quantityTaken INT,
    takeDate DATE,
    PRIMARY KEY (patientID, componentID, takeDate),
    FOREIGN KEY (patientID) REFERENCES patient(patientID),
    FOREIGN KEY (componentID) REFERENCES component(componentID)
);

-- Sample data for Patient_Component
INSERT INTO Patient_component (patientID, componentID, quantityTaken, takeDate) VALUES 
('P001', 'C001', 1, '2025-05-01'),
('P001', 'C002', 2, '2025-05-02'),
('P002', 'C001', 1, '2025-05-03');
