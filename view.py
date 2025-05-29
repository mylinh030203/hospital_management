from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLineEdit, QComboBox, QDateEdit, 
    QLabel, QMessageBox, QTabWidget, QFormLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QDate, QDateTime, Qt
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtGui import QFont

class HospitalView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hospital Management System")
        self.setGeometry(100, 100, 1200, 700)  # Slightly larger window for better spacing

        # Apply global stylesheet for consistent look
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QLabel { font-size: 12px; color: #2d3436; }
            QLineEdit, QComboBox, QDateEdit, QDateTimeEdit { 
                padding: 8px; 
                border: 1px solid #dfe6e9; 
                border-radius: 5px; 
                font-size: 12px;
                background-color: #ffffff;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDateTimeEdit:focus {
                border: 1px solid #0984e3;
            }
            QPushButton { 
                background-color: #0984e3; 
                color: white; 
                padding: 8px; 
                border-radius: 5px; 
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0652dd; }
            QTableWidget { 
                border: 1px solid #dfe6e9; 
                background-color: #ffffff; 
                font-size: 12px;
            }
            QTableWidget::item:selected { background-color: #74b9ff; }
            QTabWidget::pane { border: 1px solid #dfe6e9; background-color: #ffffff; }
            QTabBar::tab { 
                background: #dfe6e9; 
                padding: 10px; 
                border-top-left-radius: 5px; 
                border-top-right-radius: 5px;
                font-size: 12px;
            }
            QTabBar::tab:selected { 
                background: #0984e3; 
                color: white; 
            }
        """)

        # Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Register Tab
        self.register_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Add margins
        layout.setSpacing(15)  # Increase spacing between elements

        title = QLabel("Create a New Account")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("margin-bottom: 10px;")
        layout.addWidget(title)

        # Form layout for inputs
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(50, 0, 50, 0)  # Center form

        self.register_username_input = QLineEdit()
        self.register_username_input.setPlaceholderText("Enter your username")
        self.register_username_input.setMinimumHeight(35)

        self.register_password_input = QLineEdit()
        self.register_password_input.setPlaceholderText("Enter your password")
        self.register_password_input.setEchoMode(QLineEdit.Password)
        self.register_password_input.setMinimumHeight(35)

        self.register_role_input = QComboBox()
        self.register_role_input.addItems(["user", "doctor"])
        self.register_role_input.setMinimumHeight(35)

        self.register_doctor_name_input = QLineEdit()
        self.register_doctor_name_input.setPlaceholderText("Enter doctor's name")
        self.register_doctor_name_input.setMinimumHeight(35)

        self.register_specialty_input = QLineEdit()
        self.register_specialty_input.setPlaceholderText("Enter specialty")
        self.register_specialty_input.setMinimumHeight(35)

        self.register_phone_input = QLineEdit()
        self.register_phone_input.setPlaceholderText("Enter phone number")
        self.register_phone_input.setMinimumHeight(35)

        form_layout.addRow("Username:", self.register_username_input)
        form_layout.addRow("Password:", self.register_password_input)
        form_layout.addRow("Role:", self.register_role_input)
        form_layout.addRow("Doctor Name:", self.register_doctor_name_input)
        form_layout.addRow("Specialty:", self.register_specialty_input)
        form_layout.addRow("Phone:", self.register_phone_input)

        self.register_doctor_name_input.hide()
        self.register_specialty_input.hide()
        self.register_phone_input.hide()

        def toggle_doctor_fields(role):
            is_doctor = role == "doctor"
            self.register_doctor_name_input.setVisible(is_doctor)
            self.register_specialty_input.setVisible(is_doctor)
            self.register_phone_input.setVisible(is_doctor)

        self.register_role_input.currentTextChanged.connect(toggle_doctor_fields)
        layout.addLayout(form_layout)

        self.register_button = QPushButton("Register")
        self.register_button.setMinimumHeight(40)
        self.register_button.setMaximumWidth(200)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.register_widget.setLayout(layout)
        self.tabs.addTab(self.register_widget, "Register")

        # Login Tab
        self.login_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Login to Your Account")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("margin-bottom: 10px;")
        layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(50, 0, 50, 0)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(35)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        layout.addLayout(form_layout)

        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(40)
        self.login_button.setMaximumWidth(200)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.login_widget.setLayout(layout)
        self.tabs.addTab(self.login_widget, "Login")

        # Patient Management Tab
        self.patient_widget = QWidget()
        self.patient_layout = QVBoxLayout()
        self.patient_layout.setContentsMargins(20, 20, 20, 20)
        self.patient_layout.setSpacing(15)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Patient Name")
        self.name_input.setMinimumHeight(35)

        self.dob_input = QDateEdit()
        self.dob_input.setDate(QDate.currentDate().addYears(-30))
        self.dob_input.setMinimumHeight(35)

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        self.gender_combo.setMinimumHeight(35)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")
        self.address_input.setMinimumHeight(35)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")
        self.phone_input.setMinimumHeight(35)

        self.admission_date_input = QDateEdit()
        self.admission_date_input.setDate(QDate.currentDate())
        self.admission_date_input.setMinimumHeight(35)

        input_layout.addWidget(QLabel("Name:"))
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(QLabel("DOB:"))
        input_layout.addWidget(self.dob_input)
        input_layout.addWidget(QLabel("Gender:"))
        input_layout.addWidget(self.gender_combo)
        input_layout.addWidget(QLabel("Address:"))
        input_layout.addWidget(self.address_input)
        input_layout.addWidget(QLabel("Phone:"))
        input_layout.addWidget(self.phone_input)
        input_layout.addWidget(QLabel("Admission:"))
        input_layout.addWidget(self.admission_date_input)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.add_patient_button = QPushButton("Add Patient")
        self.add_patient_button.setMinimumHeight(40)
        self.update_patient_button = QPushButton("Update Patient")
        self.update_patient_button.setMinimumHeight(40)
        self.delete_patient_button = QPushButton("Delete Patient")
        self.delete_patient_button.setMinimumHeight(40)
        button_layout.addWidget(self.add_patient_button)
        button_layout.addWidget(self.update_patient_button)
        button_layout.addWidget(self.delete_patient_button)

        self.patient_table = QTableWidget()
        self.patient_table.setColumnCount(6)
        self.patient_table.setHorizontalHeaderLabels(["ID", "Name", "DOB", "Gender", "Address", "Phone"])
        self.patient_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.patient_table.horizontalHeader().setStretchLastSection(True)
        self.patient_table.setAlternatingRowColors(True)

        self.patient_layout.addLayout(input_layout)
        self.patient_layout.addLayout(button_layout)
        self.patient_layout.addWidget(self.patient_table)
        self.patient_widget.setLayout(self.patient_layout)
        self.tabs.addTab(self.patient_widget, "Patients")

        # Diagnosis Tab
        self.diagnosis_widget = QWidget()
        self.diagnosis_layout = QVBoxLayout()
        self.diagnosis_layout.setContentsMargins(20, 20, 20, 20)
        self.diagnosis_layout.setSpacing(15)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.icd_code_input = QLineEdit()
        self.icd_code_input.setPlaceholderText("ICD Code")
        self.icd_code_input.setMinimumHeight(35)

        self.disease_name_input = QLineEdit()
        self.disease_name_input.setPlaceholderText("Disease Name")
        self.disease_name_input.setMinimumHeight(35)

        self.diagnosis_date_input = QDateTimeEdit()
        self.diagnosis_date_input.setDateTime(QDateTime.currentDateTime())
        self.diagnosis_date_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.diagnosis_date_input.setMinimumHeight(35)

        input_layout.addWidget(QLabel("ICD Code:"))
        input_layout.addWidget(self.icd_code_input)
        input_layout.addWidget(QLabel("Disease:"))
        input_layout.addWidget(self.disease_name_input)
        input_layout.addWidget(QLabel("Date:"))
        input_layout.addWidget(self.diagnosis_date_input)

        self.add_diagnosis_button = QPushButton("Add Diagnosis")
        self.add_diagnosis_button.setMinimumHeight(40)
        self.add_diagnosis_button.setMaximumWidth(200)

        self.diagnosis_table = QTableWidget()
        self.diagnosis_table.setColumnCount(4)
        self.diagnosis_table.setHorizontalHeaderLabels(["ID", "ICD Code", "Disease Name", "Date"])
        self.diagnosis_table.horizontalHeader().setStretchLastSection(True)
        self.diagnosis_table.setAlternatingRowColors(True)

        self.diagnosis_layout.addLayout(input_layout)
        self.diagnosis_layout.addWidget(self.add_diagnosis_button, alignment=Qt.AlignCenter)
        self.diagnosis_layout.addWidget(self.diagnosis_table)
        self.diagnosis_widget.setLayout(self.diagnosis_layout)
        self.tabs.addTab(self.diagnosis_widget, "Diagnoses")

        # Prescription Tab
        self.prescription_widget = QWidget()
        self.prescription_layout = QVBoxLayout()
        self.prescription_layout.setContentsMargins(20, 20, 20, 20)
        self.prescription_layout.setSpacing(15)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.medication_input = QLineEdit()
        self.medication_input.setPlaceholderText("Medication Name")
        self.medication_input.setMinimumHeight(35)

        self.dosage_input = QLineEdit()
        self.dosage_input.setPlaceholderText("Dosage")
        self.dosage_input.setMinimumHeight(35)

        self.instructions_input = QLineEdit()
        self.instructions_input.setPlaceholderText("Instructions")
        self.instructions_input.setMinimumHeight(35)

        self.prescription_date_input = QDateEdit()
        self.prescription_date_input.setDate(QDate.currentDate())
        self.prescription_date_input.setMinimumHeight(35)

        self.doctor_combo = QComboBox()
        self.doctor_combo.setMinimumHeight(35)

        input_layout.addWidget(QLabel("Medication:"))
        input_layout.addWidget(self.medication_input)
        input_layout.addWidget(QLabel("Dosage:"))
        input_layout.addWidget(self.dosage_input)
        input_layout.addWidget(QLabel("Instructions:"))
        input_layout.addWidget(self.instructions_input)
        input_layout.addWidget(QLabel("Doctor:"))
        input_layout.addWidget(self.doctor_combo)
        input_layout.addWidget(QLabel("Date:"))
        input_layout.addWidget(self.prescription_date_input)

        self.add_prescription_button = QPushButton("Add Prescription")
        self.add_prescription_button.setMinimumHeight(40)
        self.add_prescription_button.setMaximumWidth(200)

        self.prescription_table = QTableWidget()
        self.prescription_table.setColumnCount(6)  # Adjusted for Doctor column
        self.prescription_table.setHorizontalHeaderLabels(["ID", "Doctor", "Medication", "Dosage", "Instructions", "Date"])
        self.prescription_table.horizontalHeader().setStretchLastSection(True)
        self.prescription_table.setAlternatingRowColors(True)

        self.prescription_layout.addLayout(input_layout)
        self.prescription_layout.addWidget(self.add_prescription_button, alignment=Qt.AlignCenter)
        self.prescription_layout.addWidget(self.prescription_table)
        self.prescription_widget.setLayout(self.prescription_layout)
        self.tabs.addTab(self.prescription_widget, "Prescriptions")

        # Visit Tab
        self.visit_widget = QWidget()
        self.visit_layout = QVBoxLayout()
        self.visit_layout.setContentsMargins(20, 20, 20, 20)
        self.visit_layout.setSpacing(15)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.visit_date_input = QDateTimeEdit()
        self.visit_date_input.setDateTime(QDateTime.currentDateTime())
        self.visit_date_input.setMinimumHeight(35)

        self.visit_notes_input = QLineEdit()
        self.visit_notes_input.setPlaceholderText("Notes")
        self.visit_notes_input.setMinimumHeight(35)

        self.visit_doctor_combo = QComboBox()
        self.visit_doctor_combo.setMinimumHeight(35)

        input_layout.addWidget(QLabel("Date:"))
        input_layout.addWidget(self.visit_date_input)
        input_layout.addWidget(QLabel("Notes:"))
        input_layout.addWidget(self.visit_notes_input)
        input_layout.addWidget(QLabel("Doctor:"))
        input_layout.addWidget(self.visit_doctor_combo)

        self.add_visit_button = QPushButton("Add Visit")
        self.add_visit_button.setMinimumHeight(40)
        self.add_visit_button.setMaximumWidth(200)

        self.visit_table = QTableWidget()
        self.visit_table.setColumnCount(4)
        self.visit_table.setHorizontalHeaderLabels(["ID", "Doctor", "Date", "Notes"])
        self.visit_table.horizontalHeader().setStretchLastSection(True)
        self.visit_table.setAlternatingRowColors(True)

        self.visit_layout.addLayout(input_layout)
        self.visit_layout.addWidget(self.add_visit_button, alignment=Qt.AlignCenter)
        self.visit_layout.addWidget(self.visit_table)
        self.visit_widget.setLayout(self.visit_layout)
        self.tabs.addTab(self.visit_widget, "Visits")

        # Appointment Tab
        self.appointment_widget = QWidget()
        self.appointment_layout = QVBoxLayout()
        self.appointment_layout.setContentsMargins(20, 20, 20, 20)
        self.appointment_layout.setSpacing(15)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.appointment_date_input = QDateTimeEdit()
        self.appointment_date_input.setDateTime(QDateTime.currentDateTime())
        self.appointment_date_input.setMinimumHeight(35)

        self.appointment_status_combo = QComboBox()
        self.appointment_status_combo.addItems(["Scheduled", "Cancelled", "Completed"])
        self.appointment_status_combo.setMinimumHeight(35)

        self.appointment_doctor_combo = QComboBox()
        self.appointment_doctor_combo.setMinimumHeight(35)

        input_layout.addWidget(QLabel("Date:"))
        input_layout.addWidget(self.appointment_date_input)
        input_layout.addWidget(QLabel("Status:"))
        input_layout.addWidget(self.appointment_status_combo)
        input_layout.addWidget(QLabel("Doctor:"))
        input_layout.addWidget(self.appointment_doctor_combo)

        self.add_appointment_button = QPushButton("Add Appointment")
        self.add_appointment_button.setMinimumHeight(40)
        self.add_appointment_button.setMaximumWidth(200)

        self.appointment_table = QTableWidget()
        self.appointment_table.setColumnCount(4)
        self.appointment_table.setHorizontalHeaderLabels(["ID", "Doctor", "Date", "Status"])
        self.appointment_table.horizontalHeader().setStretchLastSection(True)
        self.appointment_table.setAlternatingRowColors(True)

        self.appointment_layout.addLayout(input_layout)
        self.appointment_layout.addWidget(self.add_appointment_button, alignment=Qt.AlignCenter)
        self.appointment_layout.addWidget(self.appointment_table)
        self.appointment_widget.setLayout(self.appointment_layout)
        self.tabs.addTab(self.appointment_widget, "Appointments")

       # Statistics Tab
        self.stats_widget = QWidget()
        self.stats_layout = QVBoxLayout()
        self.stats_layout.setContentsMargins(20, 20, 20, 20)
        self.stats_layout.setSpacing(15)

        self.stats_button = QPushButton("Show Disease Statistics")
        self.stats_button.setMinimumHeight(40)
        self.stats_button.setMaximumWidth(200)

        self.stats2_button = QPushButton("Show Appointment Statistics")
        self.stats2_button.setMinimumHeight(40)
        self.stats2_button.setMaximumWidth(200)

        # Create a horizontal layout for buttons to place them side by side
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addWidget(self.stats_button)
        button_layout.addWidget(self.stats2_button)
        button_layout.addStretch()  # Add stretch to center buttons

        self.stats_layout.addLayout(button_layout)
        self.stats_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.stats_widget.setLayout(self.stats_layout)
        self.tabs.addTab(self.stats_widget, "Statistics")

        # Search ICD Code Tab
        # self.icd_search_widget = QWidget()
        # self.icd_search_layout = QVBoxLayout()
        # self.icd_search_layout.setContentsMargins(20, 20, 20, 20)
        # self.icd_search_layout.setSpacing(15)

        # self.icd_search_input = QLineEdit()
        # self.icd_search_input.setPlaceholderText("Search by ICD code")
        # self.icd_search_input.setMinimumHeight(35)
        # self.icd_search_input.setMaximumWidth(300)

        # self.icd_search_button = QPushButton("Search")
        # self.icd_search_button.setMinimumHeight(40)
        # self.icd_search_button.setMaximumWidth(200)

        # self.results = QLabel()
        # self.results.setText("")
        # self.results.setStyleSheet("font-size: 12px; color: #2d3436;")

        # self.icd_search_layout.addWidget(self.icd_search_input, alignment=Qt.AlignCenter)
        # self.icd_search_layout.addWidget(self.icd_search_button, alignment=Qt.AlignCenter)
        # self.icd_search_layout.addWidget(self.results, alignment=Qt.AlignCenter)
        # self.icd_search_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # self.icd_search_widget.setLayout(self.icd_search_layout)
        # self.tabs.addTab(self.icd_search_widget, "Search ICD Code")

        # Search ICD Code Tab
        self.icd_search_widget = QWidget()
        self.icd_search_layout = QVBoxLayout()
        self.icd_search_layout.setContentsMargins(20, 20, 20, 20)
        self.icd_search_layout.setSpacing(15)

        self.icd_search_input = QLineEdit()
        self.icd_search_input.setPlaceholderText("Search by ICD code")
        self.icd_search_input.setMinimumHeight(35)
        self.icd_search_input.setMaximumWidth(300)

        self.icd_search_button = QPushButton("Search")
        self.icd_search_button.setMinimumHeight(40)
        self.icd_search_button.setMaximumWidth(200)

        self.results = QLabel()
        self.results.setText("")
        self.results.setStyleSheet("font-size: 14px; color: #2d3436;")  # Increased font size to 14px
        self.results.setWordWrap(True)  # Enable word wrapping
        self.results.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # Align text to top-left
        self.results.setMinimumHeight(100)  # Ensure enough space for multiple lines
        self.results.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow label to expand

        self.icd_search_layout.addWidget(self.icd_search_input, alignment=Qt.AlignCenter)
        self.icd_search_layout.addWidget(self.icd_search_button, alignment=Qt.AlignCenter)
        self.icd_search_layout.addWidget(self.results, alignment=Qt.AlignCenter)
        self.icd_search_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.icd_search_widget.setLayout(self.icd_search_layout)
        self.tabs.addTab(self.icd_search_widget, "Search ICD Code")

    # Methods remain unchanged
    def show_patient_table_with_one(self, patient):
        self.patient_table.setVisible(True)
        self.patient_table.setRowCount(1)
        self.patient_table.setItem(0, 0, QTableWidgetItem(str(patient.id)))
        self.patient_table.setItem(0, 1, QTableWidgetItem(patient.name))
        self.patient_table.setItem(0, 2, QTableWidgetItem(patient.date_of_birth))
        self.patient_table.setItem(0, 3, QTableWidgetItem(patient.gender))
        self.patient_table.setItem(0, 4, QTableWidgetItem(patient.address))
        self.patient_table.setItem(0, 5, QTableWidgetItem(patient.phone))

    def display_patients(self, patients):
        self.patient_table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            for col, data in enumerate(patient):
                self.patient_table.setItem(row, col, QTableWidgetItem(str(data)))

    def display_diagnoses(self, diagnoses):
        self.diagnosis_table.setRowCount(len(diagnoses))
        for row, diagnosis in enumerate(diagnoses):
            for col, data in enumerate(diagnosis):
                self.diagnosis_table.setItem(row, col, QTableWidgetItem(str(data)))

    def display_prescriptions(self, prescriptions):
        self.prescription_table.setRowCount(len(prescriptions))
        for row, prescription in enumerate(prescriptions):
            for col, data in enumerate(prescription):
                self.prescription_table.setItem(row, col, QTableWidgetItem(str(data)))

    def display_visits(self, visits):
        self.visit_table.setRowCount(len(visits))
        for row, visit in enumerate(visits):
            for col, data in enumerate(visit):
                self.visit_table.setItem(row, col, QTableWidgetItem(str(data)))

    def display_appointments(self, appointments):
        self.appointment_table.setRowCount(len(appointments))
        for row, appointment in enumerate(appointments):
            for col, data in enumerate(appointment):
                self.appointment_table.setItem(row, col, QTableWidgetItem(str(data)))

    def populate_doctor_combo(self, doctors):
        self.doctor_combo.clear()
        self.visit_doctor_combo.clear()
        self.appointment_doctor_combo.clear()
        for doctor in doctors:
            display_text = f"{doctor.name} ({doctor.specialty})"
            self.doctor_combo.addItem(display_text, doctor.id)
            self.visit_doctor_combo.addItem(display_text, doctor.id)
            self.appointment_doctor_combo.addItem(display_text, doctor.id)

    def get_patient_input(self):
        return (
            self.name_input.text(),
            self.dob_input.date().toString("yyyy-MM-dd"),
            self.gender_combo.currentText(),
            self.address_input.text(),
            self.phone_input.text(),
            self.admission_date_input.date().toString("yyyy-MM-dd")
        )

    def get_diagnosis_input(self):
        return (
            self.icd_code_input.text(),
            self.disease_name_input.text(),
            self.diagnosis_date_input.date().toString("yyyy-MM-dd")
        )

    def get_prescription_input(self):
        return (
            self.medication_input.text(),
            self.dosage_input.text(),
            self.instructions_input.text(),
            self.prescription_date_input.date().toString("yyyy-MM-dd"),
            self.doctor_combo.currentData()
        )

    def get_visit_input(self):
        return (
            self.visit_date_input.dateTime().toString("yyyy-MM-dd hh:mm:ss"),
            self.visit_notes_input.text(),
            self.visit_doctor_combo.currentData()
        )

    def get_appointment_input(self):
        return (
            self.appointment_date_input.dateTime().toString("yyyy-MM-dd hh:mm:ss"),
            self.appointment_status_combo.currentText(),
            self.appointment_doctor_combo.currentData()
        )

    def set_selected_patient(self, id, name, dob, gender, address, phone, admission_date):
        self.name_input.setText(name)
        self.dob_input.setDate(QDate.fromString(dob, "yyyy-MM-dd"))
        self.gender_combo.setCurrentText(gender)
        self.address_input.setText(address)
        self.phone_input.setText(phone)
        self.admission_date_input.setDate(QDate.fromString(admission_date, "yyyy-MM-dd"))

    def clear_patient_inputs(self):
        self.name_input.clear()
        self.dob_input.setDate(QDate.currentDate().addYears(-30))
        self.address_input.clear()
        self.phone_input.clear()
        self.admission_date_input.setDate(QDate.currentDate())

    def clear_diagnosis_inputs(self):
        self.icd_code_input.clear()
        self.disease_name_input.clear()
        self.diagnosis_date_input.setDate(QDate.currentDate())

    def clear_prescription_inputs(self):
        self.medication_input.clear()
        self.dosage_input.clear()
        self.instructions_input.clear()
        self.prescription_date_input.setDate(QDate.currentDate())

    def clear_visit_inputs(self):
        self.visit_date_input.setDateTime(QDateTime.currentDateTime())
        self.visit_notes_input.clear()

    def clear_appointment_inputs(self):
        self.appointment_date_input.setDateTime(QDateTime.currentDateTime())
        self.appointment_status_combo.setCurrentText("Scheduled")

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)