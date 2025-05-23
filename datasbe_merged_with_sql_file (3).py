import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import csv
from datetime import datetime

# Constants
DATABASE_FILE = 'LAB'  # Ensure this points to the correct database file

# Function to create the database and tables
def create_database():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS laboratorian (
                            laboratorianID INTEGER PRIMARY KEY,
                            firstName TEXT NOT NULL,
                            middleName TEXT,
                            lastName TEXT NOT NULL,
                            phone INTEGER NOT NULL,
                            address TEXT,
                            UNIQUE(firstName, lastName, phone))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS patient (
                            patientID VARCHAR(9) PRIMARY KEY,
                            firstName TEXT,
                            middleName TEXT,
                            lastName TEXT,
                            phone VARCHAR(13),
                            city TEXT,
                            street TEXT,
                            country TEXT,
                            birthdate DATE,
                            job TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS medicalTest (
                            testID VARCHAR(9) PRIMARY KEY,
                            name TEXT,
                            price INT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS testResult (
                            resultID VARCHAR(9) PRIMARY KEY,
                            testID VARCHAR(9),
                            patientID VARCHAR(9),
                            laboratorianID INTEGER,
                            testDate DATE,
                            result TEXT,
                            FOREIGN KEY (testID) REFERENCES medicalTest(testID),
                            FOREIGN KEY (patientID) REFERENCES patient(patientID),
                            FOREIGN KEY (laboratorianID) REFERENCES laboratorian(laboratorianID))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS component (
                            componentID VARCHAR(9) PRIMARY KEY,
                            componentName TEXT,
                            availableQuantity INT,
                            minQuantity INT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS MedicalTest_component (
                            testID VARCHAR(9),
                            componentID VARCHAR(9),
                            quantityUsed INT,
                            PRIMARY KEY (testID, componentID),
                            FOREIGN KEY (testID) REFERENCES medicalTest(testID),
                            FOREIGN KEY (componentID) REFERENCES component(componentID))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Patient_component (
                            patientID VARCHAR(9),
                            componentID VARCHAR(9),
                            quantityTaken INT,
                            takeDate DATE,
                            PRIMARY KEY (patientID, componentID, takeDate),
                            FOREIGN KEY (patientID) REFERENCES patient(patientID),
                            FOREIGN KEY (componentID) REFERENCES component(componentID))''')

# Function to insert a new laboratorian
def insert_laboratorian():
    laboratorianID = laboratorianID_entry.get()
    firstName = firstName_entry.get()
    middleName = middleName_entry.get()
    lastName = lastName_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()

    if not laboratorianID or not firstName or not lastName or not phone or not address:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    # Check if laboratorianID is an integer
    if not laboratorianID.isdigit():
        messagebox.showerror("Error", "Laboratorian ID must be an integer.")
        return

    laboratorianID = int(laboratorianID)

    # Check if phone is an integer
    if not phone.isdigit():
        messagebox.showerror("Error", "Phone number must be an integer.")
        return

    phone = int(phone)

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO laboratorian (laboratorianID, firstName, middleName, lastName, phone, address) VALUES (?, ?, ?, ?, ?, ?)",
                           (laboratorianID, firstName, middleName, lastName, phone, address))
            conn.commit()
            messagebox.showinfo("Success", "Laboratorian added successfully!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Error: {e}")

# Function to insert a new patient
def insert_patient():
    patientID = patientID_entry.get()
    firstName = firstName_entry.get()
    middleName = middleName_entry.get()
    lastName = lastName_entry.get()
    phone = phone_entry.get()
    city = city_entry.get()
    street = street_entry.get()
    country = country_entry.get()
    birthdate = birthdate_entry.get()
    job = job_entry.get()

    if not patientID or not firstName or not lastName or not phone or not city or not street or not country or not birthdate or not job:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    # Check if phone is an integer
    if not phone.isdigit():
        messagebox.showerror("Error", "Phone number must be an integer.")
        return

    phone = int(phone)

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO patient (patientID, firstName, middleName, lastName, phone, city, street, country, birthdate, job) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (patientID, firstName, middleName, lastName, phone, city, street, country, birthdate, job))
            conn.commit()
            messagebox.showinfo("Success", "Patient added successfully!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Error: {e}")

# Function to insert a new medical test
def insert_medical_test():
    testID = testID_entry.get()
    name = name_entry.get()
    price = price_entry.get()

    if not testID or not name or not price:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    # Check if price is an integer
    if not price.isdigit():
        messagebox.showerror("Error", "Price must be an integer.")
        return

    price = int(price)

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO medicalTest (testID, name, price) VALUES (?, ?, ?)",
                           (testID, name, price))
            conn.commit()
            messagebox.showinfo("Success", "Medical test added successfully!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Error: {e}")

# Function to insert a new component
def insert_component():
    componentID = componentID_entry.get()
    componentName = componentName_entry.get()
    availableQuantity = availableQuantity_entry.get()
    minQuantity = minQuantity_entry.get()

    if not componentID or not componentName or not availableQuantity or not minQuantity:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    # Check if quantities are integers
    if not availableQuantity.isdigit() or not minQuantity.isdigit():
        messagebox.showerror("Error", "Quantities must be integers.")
        return

    availableQuantity = int(availableQuantity)
    minQuantity = int(minQuantity)

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO component (componentID, componentName, availableQuantity, minQuantity) VALUES (?, ?, ?, ?)",
                           (componentID, componentName, availableQuantity, minQuantity))
            conn.commit()
            messagebox.showinfo("Success", "Component added successfully!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Error: {e}")

# Function to insert a new test result
def insert_test_result():
    resultID = resultID_entry.get()
    testID = testID_entry.get()
    patientID = patientID_entry.get()
    laboratorianID = laboratorianID_entry.get()
    testDate = testDate_entry.get()
    result = result_entry.get()

    if not resultID or not testID or not patientID or not laboratorianID or not testDate or not result:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO testResult (resultID, testID, patientID, laboratorianID, testDate, result)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (resultID, testID, patientID, laboratorianID, testDate, result))
            conn.commit()
            messagebox.showinfo("Success", "Test result added successfully!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Error: {e}")

# Function to list patients who performed CBC test in the last year
def list_cbc_patients():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.firstName, p.lastName
            FROM patient p
            JOIN testResult tr ON p.patientID = tr.patientID
            JOIN medicalTest mt ON tr.testID = mt.testID
            WHERE mt.name = 'CBC' AND tr.testDate BETWEEN DATE('now', '-1 year') AND DATE('now');
        """)
        records = cursor.fetchall()

    listbox.delete(0, tk.END)  # Clear the listbox before displaying new data
    for record in records:
        listbox.insert(tk.END, f"Name: {record[0]} {record[1]}")

# Function to list components that are less than the minimum quantity
def list_low_quantity_components():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT componentName
            FROM component
            WHERE availableQuantity < minQuantity;
        """)
        records = cursor.fetchall()

    listbox.delete(0, tk.END)  # Clear the listbox before displaying new data
    for record in records:
        listbox.insert(tk.END, f"Component: {record[0]}")

# Function to list the total money paid by a patient in the last three years
def list_total_paid_by_patient():
    patientID = simpledialog.askstring("Input", "Enter patient ID:")
    if not patientID:
        messagebox.showerror("Error", "Patient ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(mt.price) AS totalPaid
            FROM testResult tr
            JOIN medicalTest mt ON tr.testID = mt.testID
            WHERE tr.patientID = ? AND tr.testDate BETWEEN DATE('now', '-3 years') AND DATE('now');
        """, (patientID,))
        total_paid = cursor.fetchone()[0]

    if total_paid:
        messagebox.showinfo("Total Paid", f"Total money paid by patient {patientID} in the last three years: {total_paid}")
    else:
        messagebox.showinfo("Total Paid", f"No payments found for patient {patientID} in the last three years.")

# Function to update a patient's information
def update_patient():
    patientID = simpledialog.askstring("Input", "Enter patient ID:")
    if not patientID:
        messagebox.showerror("Error", "Patient ID is required.")
        return

    firstName = simpledialog.askstring("Input", "Enter new first name:")
    middleName = simpledialog.askstring("Input", "Enter new middle name (optional):")
    lastName = simpledialog.askstring("Input", "Enter new last name:")
    phone = simpledialog.askstring("Input", "Enter new phone number:")
    city = simpledialog.askstring("Input", "Enter new city:")
    street = simpledialog.askstring("Input", "Enter new street:")
    country = simpledialog.askstring("Input", "Enter new country:")
    birthdate = simpledialog.askstring("Input", "Enter new birthdate (YYYY-MM-DD):")
    job = simpledialog.askstring("Input", "Enter new job:")

    if not firstName or not lastName or not phone or not city or not street or not country or not birthdate or not job:
        messagebox.showerror("Error", "All fields except middle name are required.")
        return

    # Check if phone is an integer
    if not phone.isdigit():
        messagebox.showerror("Error", "Phone number must be an integer.")
        return

    phone = int(phone)

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE patient
                SET firstName = ?, middleName = ?, lastName = ?, phone = ?, city = ?, street = ?, country = ?, birthdate = ?, job = ?
                WHERE patientID = ?
            """, (firstName, middleName, lastName, phone, city, street, country, birthdate, job, patientID))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "No patient found with the given ID.")
            else:
                messagebox.showinfo("Success", "Patient information updated successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating patient information: {e}")

# Function to delete a laboratorian
def delete_laboratorian():
    laboratorianID = simpledialog.askstring("Input", "Enter laboratorian ID to delete:")
    if not laboratorianID:
        messagebox.showerror("Error", "Laboratorian ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM laboratorian WHERE laboratorianID = ?", (laboratorianID,))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "No laboratorian found with the given ID.")
        else:
            messagebox.showinfo("Success", "Laboratorian deleted successfully!")

# Function to delete a patient
def delete_patient():
    patientID = simpledialog.askstring("Input", "Enter patient ID to delete:")
    if not patientID:
        messagebox.showerror("Error", "Patient ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patient WHERE patientID = ?", (patientID,))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "No patient found with the given ID.")
        else:
            messagebox.showinfo("Success", "Patient deleted successfully!")

# Function to delete a medical test
def delete_medical_test():
    testID = simpledialog.askstring("Input", "Enter test ID to delete:")
    if not testID:
        messagebox.showerror("Error", "Test ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medicalTest WHERE testID = ?", (testID,))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "No test found with the given ID.")
        else:
            messagebox.showinfo("Success", "Medical test deleted successfully!")

# Function to delete a component
def delete_component():
    componentID = simpledialog.askstring("Input", "Enter component ID to delete:")
    if not componentID:
        messagebox.showerror("Error", "Component ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM component WHERE componentID = ?", (componentID,))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "No component found with the given ID.")
        else:
            messagebox.showinfo("Success", "Component deleted successfully!")

# Function to delete a test result
def delete_test_result():
    resultID = simpledialog.askstring("Input", "Enter result ID to delete:")
    if not resultID:
        messagebox.showerror("Error", "Result ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM testResult WHERE resultID = ?", (resultID,))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showerror("Error", "No test result found with the given ID.")
        else:
            messagebox.showinfo("Success", "Test result deleted successfully!")

# Function to search for a laboratorian
def search_laboratorian():
    laboratorianID = simpledialog.askstring("Input", "Enter laboratorian ID to search:")
    if not laboratorianID:
        messagebox.showerror("Error", "Laboratorian ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM laboratorian WHERE laboratorianID = ?", (laboratorianID,))
        record = cursor.fetchone()
        if record:
            messagebox.showinfo("Search Result", f"ID: {record[0]}, Name: {record[1]} {record[2]} {record[3]}, Phone: {record[4]}, Address: {record[5]}")
        else:
            messagebox.showerror("Error", "No laboratorian found with the given ID.")

# Function to search for a patient
def search_patient():
    patientID = simpledialog.askstring("Input", "Enter patient ID to search:")
    if not patientID:
        messagebox.showerror("Error", "Patient ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient WHERE patientID = ?", (patientID,))
        record = cursor.fetchone()
        if record:
            messagebox.showinfo("Search Result", f"ID: {record[0]}, Name: {record[1]} {record[2]} {record[3]}, Phone: {record[4]}, Address: {record[5]} {record[6]} {record[7]}, Birthdate: {record[8]}, Job: {record[9]}")
        else:
            messagebox.showerror("Error", "No patient found with the given ID.")

# Function to search for a medical test
def search_medical_test():
    testID = simpledialog.askstring("Input", "Enter test ID to search:")
    if not testID:
        messagebox.showerror("Error", "Test ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicalTest WHERE testID = ?", (testID,))
        record = cursor.fetchone()
        if record:
            messagebox.showinfo("Search Result", f"ID: {record[0]}, Name: {record[1]}, Price: {record[2]}")
        else:
            messagebox.showerror("Error", "No test found with the given ID.")

# Function to search for a component
def search_component():
    componentID = simpledialog.askstring("Input", "Enter component ID to search:")
    if not componentID:
        messagebox.showerror("Error", "Component ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM component WHERE componentID = ?", (componentID,))
        record = cursor.fetchone()
        if record:
            messagebox.showinfo("Search Result", f"ID: {record[0]}, Name: {record[1]}, Available Quantity: {record[2]}, Minimum Quantity: {record[3]}")
        else:
            messagebox.showerror("Error", "No component found with the given ID.")

# Function to search for a test result
def search_test_result():
    resultID = simpledialog.askstring("Input", "Enter result ID to search:")
    if not resultID:
        messagebox.showerror("Error", "Result ID is required.")
        return

    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM testResult WHERE resultID = ?", (resultID,))
        record = cursor.fetchone()
        if record:
            messagebox.showinfo("Search Result", f"ID: {record[0]}, Test ID: {record[1]}, Patient ID: {record[2]}, Laboratorian ID: {record[3]}, Test Date: {record[4]}, Result: {record[5]}")
        else:
            messagebox.showerror("Error", "No test result found with the given ID.")

# Function to export data to CSV
def export_to_csv(table_name):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

    if not rows:
        messagebox.showerror("Error", "No data found in the table.")
        return

    with open(f"{table_name}.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([i[0] for i in cursor.description])  # Write headers
        writer.writerows(rows)

    messagebox.showinfo("Success", f"Data exported to {table_name}.csv successfully!")

# Create the main window
root = tk.Tk()
root.title("LAB Database Manager")
root.geometry("1200x800")

# Create input fields for laboratorian
laboratorianID_label = tk.Label(root, text="Laboratorian ID:")
laboratorianID_label.grid(row=0, column=0, padx=10, pady=5)
laboratorianID_entry = tk.Entry(root)
laboratorianID_entry.grid(row=0, column=1, padx=10, pady=5)

firstName_label = tk.Label(root, text="First Name:")
firstName_label.grid(row=1, column=0, padx=10, pady=5)
firstName_entry = tk.Entry(root)
firstName_entry.grid(row=1, column=1, padx=10, pady=5)

middleName_label = tk.Label(root, text="Middle Name:")
middleName_label.grid(row=2, column=0, padx=10, pady=5)
middleName_entry = tk.Entry(root)
middleName_entry.grid(row=2, column=1, padx=10, pady=5)

lastName_label = tk.Label(root, text="Last Name:")
lastName_label.grid(row=3, column=0, padx=10, pady=5)
lastName_entry = tk.Entry(root)
lastName_entry.grid(row=3, column=1, padx=10, pady=5)

phone_label = tk.Label(root, text="Phone:")
phone_label.grid(row=4, column=0, padx=10, pady=5)
phone_entry = tk.Entry(root)
phone_entry.grid(row=4, column=1, padx=10, pady=5)

address_label = tk.Label(root, text="Address:")
address_label.grid(row=5, column=0, padx=10, pady=5)
address_entry = tk.Entry(root)
address_entry.grid(row=5, column=1, padx=10, pady=5)

# Create input fields for patient
patientID_label = tk.Label(root, text="Patient ID:")
patientID_label.grid(row=0, column=2, padx=10, pady=5)
patientID_entry = tk.Entry(root)
patientID_entry.grid(row=0, column=3, padx=10, pady=5)

city_label = tk.Label(root, text="City:")
city_label.grid(row=5, column=2, padx=10, pady=5)
city_entry = tk.Entry(root)
city_entry.grid(row=5, column=3, padx=10, pady=5)

street_label = tk.Label(root, text="Street:")
street_label.grid(row=6, column=2, padx=10, pady=5)
street_entry = tk.Entry(root)
street_entry.grid(row=6, column=3, padx=10, pady=5)

country_label = tk.Label(root, text="Country:")
country_label.grid(row=7, column=2, padx=10, pady=5)
country_entry = tk.Entry(root)
country_entry.grid(row=7, column=3, padx=10, pady=5)

birthdate_label = tk.Label(root, text="Birthdate (YYYY-MM-DD):")
birthdate_label.grid(row=8, column=2, padx=10, pady=5)
birthdate_entry = tk.Entry(root)
birthdate_entry.grid(row=8, column=3, padx=10, pady=5)

job_label = tk.Label(root, text="Job:")
job_label.grid(row=9, column=2, padx=10, pady=5)
job_entry = tk.Entry(root)
job_entry.grid(row=9, column=3, padx=10, pady=5)

# Create input fields for medical test
testID_label = tk.Label(root, text="Test ID:")
testID_label.grid(row=0, column=4, padx=10, pady=5)
testID_entry = tk.Entry(root)
testID_entry.grid(row=0, column=5, padx=10, pady=5)

name_label = tk.Label(root, text="Test Name:")
name_label.grid(row=1, column=4, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=5, padx=10, pady=5)

price_label = tk.Label(root, text="Price:")
price_label.grid(row=2, column=4, padx=10, pady=5)
price_entry = tk.Entry(root)
price_entry.grid(row=2, column=5, padx=10, pady=5)

# Create input fields for component
componentID_label = tk.Label(root, text="Component ID:")
componentID_label.grid(row=0, column=6, padx=10, pady=5)
componentID_entry = tk.Entry(root)
componentID_entry.grid(row=0, column=7, padx=10, pady=5)

componentName_label = tk.Label(root, text="Component Name:")
componentName_label.grid(row=1, column=6, padx=10, pady=5)
componentName_entry = tk.Entry(root)
componentName_entry.grid(row=1, column=7, padx=10, pady=5)

availableQuantity_label = tk.Label(root, text="Available Quantity:")
availableQuantity_label.grid(row=2, column=6, padx=10, pady=5)
availableQuantity_entry = tk.Entry(root)
availableQuantity_entry.grid(row=2, column=7, padx=10, pady=5)

minQuantity_label = tk.Label(root, text="Minimum Quantity:")
minQuantity_label.grid(row=3, column=6, padx=10, pady=5)
minQuantity_entry = tk.Entry(root)
minQuantity_entry.grid(row=3, column=7, padx=10, pady=5)

# Create input fields for test result
resultID_label = tk.Label(root, text="Result ID:")
resultID_label.grid(row=0, column=8, padx=10, pady=5)
resultID_entry = tk.Entry(root)
resultID_entry.grid(row=0, column=9, padx=10, pady=5)

testDate_label = tk.Label(root, text="Test Date (YYYY-MM-DD):")
testDate_label.grid(row=1, column=8, padx=10, pady=5)
testDate_entry = tk.Entry(root)
testDate_entry.grid(row=1, column=9, padx=10, pady=5)

result_label = tk.Label(root, text="Result:")
result_label.grid(row=2, column=8, padx=10, pady=5)
result_entry = tk.Entry(root)
result_entry.grid(row=2, column=9, padx=10, pady=5)

# Create buttons for actions
insert_laboratorian_button = tk.Button(root, text="Insert Laboratorian", command=insert_laboratorian)
insert_laboratorian_button.grid(row=6, column=0, columnspan=2, pady=10)

insert_patient_button = tk.Button(root, text="Insert Patient", command=insert_patient)
insert_patient_button.grid(row=6, column=2, columnspan=2, pady=10)

insert_medical_test_button = tk.Button(root, text="Insert Medical Test", command=insert_medical_test)
insert_medical_test_button.grid(row=6, column=4, columnspan=2, pady=10)

insert_component_button = tk.Button(root, text="Insert Component", command=insert_component)
insert_component_button.grid(row=6, column=6, columnspan=2, pady=10)

insert_test_result_button = tk.Button(root, text="Insert Test Result", command=insert_test_result)
insert_test_result_button.grid(row=6, column=8, columnspan=2, pady=10)

update_patient_button = tk.Button(root, text="Update Patient", command=update_patient)
update_patient_button.grid(row=7, column=0, columnspan=2, pady=10)

list_cbc_patients_button = tk.Button(root, text="List CBC Patients", command=list_cbc_patients)
list_cbc_patients_button.grid(row=9, column=0, columnspan=2, pady=10)

list_low_quantity_components_button = tk.Button(root, text="List Low Quantity Components", command=list_low_quantity_components)
list_low_quantity_components_button.grid(row=10, column=0, columnspan=2, pady=10)

list_total_paid_by_patient_button = tk.Button(root, text="Total Paid by Patient", command=list_total_paid_by_patient)
list_total_paid_by_patient_button.grid(row=11, column=0, columnspan=2, pady=10)

# Buttons for deleting records
delete_laboratorian_button = tk.Button(root, text="Delete Laboratorian", command=delete_laboratorian)
delete_laboratorian_button.grid(row=7, column=2, columnspan=2, pady=10)

delete_patient_button = tk.Button(root, text="Delete Patient", command=delete_patient)
delete_patient_button.grid(row=7, column=4, columnspan=2, pady=10)

delete_medical_test_button = tk.Button(root, text="Delete Medical Test", command=delete_medical_test)
delete_medical_test_button.grid(row=7, column=6, columnspan=2, pady=10)

delete_component_button = tk.Button(root, text="Delete Component", command=delete_component)
delete_component_button.grid(row=7, column=8, columnspan=2, pady=10)

delete_test_result_button = tk.Button(root, text="Delete Test Result", command=delete_test_result)
delete_test_result_button.grid(row=7, column=10, columnspan=2, pady=10)

# Buttons for searching records
search_laboratorian_button = tk.Button(root, text="Search Laboratorian", command=search_laboratorian)
search_laboratorian_button.grid(row=8, column=0, columnspan=2, pady=10)

search_patient_button = tk.Button(root, text="Search Patient", command=search_patient)
search_patient_button.grid(row=8, column=2, columnspan=2, pady=10)

search_medical_test_button = tk.Button(root, text="Search Medical Test", command=search_medical_test)
search_medical_test_button.grid(row=8, column=4, columnspan=2, pady=10)

search_component_button = tk.Button(root, text="Search Component", command=search_component)
search_component_button.grid(row=8, column=6, columnspan=2, pady=10)

search_test_result_button = tk.Button(root, text="Search Test Result", command=search_test_result)
search_test_result_button.grid(row=8, column=8, columnspan=2, pady=10)

# Buttons for exporting data to CSV
export_laboratorian_button = tk.Button(root, text="Export Laboratorian", command=lambda: export_to_csv("laboratorian"))
export_laboratorian_button.grid(row=9, column=2, columnspan=2, pady=10)

export_patient_button = tk.Button(root, text="Export Patient", command=lambda: export_to_csv("patient"))
export_patient_button.grid(row=9, column=4, columnspan=2, pady=10)

export_medical_test_button = tk.Button(root, text="Export Medical Test", command=lambda: export_to_csv("medicalTest"))
export_medical_test_button.grid(row=9, column=6, columnspan=2, pady=10)

export_component_button = tk.Button(root, text="Export Component", command=lambda: export_to_csv("component"))
export_component_button.grid(row=9, column=8, columnspan=2, pady=10)

export_test_result_button = tk.Button(root, text="Export Test Result", command=lambda: export_to_csv("testResult"))
export_test_result_button.grid(row=9, column=10, columnspan=2, pady=10)

# Create a listbox to display data
listbox = tk.Listbox(root, width=100)
listbox.grid(row=12, column=0, columnspan=10, padx=10, pady=10)

# Create the database and tables
create_database()

# Run the application
root.mainloop()