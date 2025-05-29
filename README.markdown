# Hospital Management System

## Overview
A Python-based desktop application using PyQt5 and MySQL to manage hospital operations, including user registration, patient management, diagnoses, prescriptions, visits, appointments, and statistics with role-based access (admin, doctor, user).

## Features
- **User Management**: Register/authenticate users (admin, doctor, user) with SHA-256 hashed passwords.
- **Patient Management**: Add, update, delete patients (admin/doctor roles).
- **Diagnosis/Prescription/Visit/Appointment Management**: Add and view records for selected patients.
- **Statistics**: Bar charts for disease and appointment statistics.
- **ICD Code Search**: Query ICD-10 codes via external API.
- **Role-Based Access**: Admins (full access), doctors (limited), users (view-only).

## Technologies
- Python 3.x
- PyQt5 (UI)
- MySQL Connector (database)
- Matplotlib (charts)
- Requests (API calls)

## Prerequisites
- Python 3.6+
- MySQL Server
- Dependencies:
  ```bash
  pip install mysql-connector-python pyqt5 matplotlib requests
  ```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mylinh030203/hospital_management
   cd hospital-management-system
   ```
2. Set up MySQL database `hospital_db` with the schema from the code (tables: users, doctors, patients, diagnoses, prescriptions, visits, appointments).
3. Update database credentials in `DatabaseModel.__init__`.
4. Run the application:
   ```bash
   python controller.py
   ```

## Usage
- **Default Credentials**: Admin (`admin`/`admin123`), Doctor (`doctor`/`doctor123`).
- **Register/Login**: Use "Register" or "Login" tabs to create or access accounts.
- **Manage Data**: Add/view patient records, diagnoses, prescriptions, visits, and appointments via respective tabs.
- **Statistics**: View disease/appointment charts in the "Statistics" tab.
- **ICD Search**: Search ICD-10 codes in the "Search ICD Code" tab.

## Notes
- Passwords are hashed with SHA-256 for security.
- ICD-10 API requires an internet connection.
- Ensure MySQL server is running before starting the app.

## License
MIT License