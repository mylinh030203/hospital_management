import sys
import matplotlib.pyplot as plt
from model import DatabaseModel
from entity import User, Patient, Appointment, Visit, Diagnosis, Prescription, Doctor
from view import HospitalView

class HospitalController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_user_role = None
        self.selected_patient_id = None

        # Connect signals
        self.view.register_button.clicked.connect(self.handle_register)
        self.view.login_button.clicked.connect(self.handle_login)
        self.view.add_patient_button.clicked.connect(self.handle_add_patient)
        self.view.update_patient_button.clicked.connect(self.handle_update_patient)
        self.view.delete_patient_button.clicked.connect(self.handle_delete_patient)
        self.view.add_diagnosis_button.clicked.connect(self.handle_add_diagnosis)
        self.view.add_prescription_button.clicked.connect(self.handle_add_prescription)
        self.view.add_visit_button.clicked.connect(self.handle_add_visit)
        self.view.add_appointment_button.clicked.connect(self.handle_add_appointment)
        self.view.stats_button.clicked.connect(self.handle_stats)
        self.view.stats2_button.clicked.connect(self.handle_stats_appointments)
        self.view.patient_table.itemSelectionChanged.connect(self.handle_patient_selection)
        self.view.icd_search_button.clicked.connect(self.search_icd_code)

#{'Search': [{'Name': 'I10', 'Description': 'Essential (primary) hypertension'}], 'totalResults': '1', 'Response': 'True'}
    def search_icd_code(self):
        search_term = self.view.icd_search_input.text()
        if not search_term:
            self.view.show_message("Error", "Please enter a search term")
            return
        icd_codes = self.model.get_icd_code(search_term)
        if icd_codes:
            results_text = (
                f"<b>Code:</b> {icd_codes.get('Name', 'N/A')}<br>"
                f"<b>Description:</b> {icd_codes.get('Description', 'N/A')}<br>"
                f"<b>Inclusions:</b> {icd_codes.get('Inclusions', 'N/A')}<br>"
                f"<b>ExcludesOne:</b> {icd_codes.get('ExcludesOne', 'N/A')}<br>"
                f"<b>ExcludesTwo:</b> {icd_codes.get('ExcludesTwo', 'N/A')}"
            )
            self.view.results.setText(results_text)
        else:
            self.view.show_message("Error", "No ICD codes found")

    # def handle_register(self):
    #     username = self.view.register_username_input.text()
    #     password = self.view.register_password_input.text()
    #     role = self.view.register_role_input.currentText()
    #     user = User(username, password, role)
    #     self.model.register_user(user)
    #     # self.model.register_user(username, password, role)
    #     self.view.show_message("Success", "User registered")
    #     self.view.register_username_input.clear()
    #     self.view.register_password_input.clear()
    #     self.view.register_role_input.setCurrentIndex(0)

    def handle_register(self):
        username = self.view.register_username_input.text()
        password = self.view.register_password_input.text()
        role = self.view.register_role_input.currentText()
        user = User(username, password, role)

        if role == "doctor":
            name = self.view.register_doctor_name_input.text()
            specialty = self.view.register_specialty_input.text()
            phone = self.view.register_phone_input.text()
            doctor = Doctor(name, specialty, phone, user_id=None)
            self.model.register_user(user, doctor)
        else:
            self.model.register_user(user)

        self.view.show_message("Success", "User registered")
        self.view.register_username_input.clear()
        self.view.register_password_input.clear()
        self.view.register_role_input.setCurrentIndex(0)

    def handle_login(self):
        username = self.view.username_input.text()
        password = self.view.password_input.text()
        role = self.model.authenticate_user(username, password)
        if role:
            self.current_user_role = role
            self.view.tabs.setCurrentIndex(2)
            self.update_ui_based_on_role()
            self.refresh_patient_list()
            self.refresh_doctor_list()
        else:
            self.view.show_message("Error", "Invalid credentials")

    def update_ui_based_on_role(self):
        if self.current_user_role == "user":
            self.view.update_patient_button.setEnabled(False)
            self.view.delete_patient_button.setEnabled(False)
            self.view.patient_table.setVisible(False)
            self.view.tabs.setTabEnabled(3, False)  
            self.view.tabs.setTabEnabled(4, False)  
            self.view.tabs.setTabEnabled(5, False)  
            self.view.tabs.setTabEnabled(6, False)  
        elif self.current_user_role == "doctor":
            self.view.update_patient_button.setEnabled(True)
            self.view.delete_patient_button.setEnabled(False)
            self.view.tabs.setTabEnabled(2, True)
            self.view.tabs.setTabEnabled(3, True)
            self.view.tabs.setTabEnabled(4, True)
            self.view.tabs.setTabEnabled(5, True)
            self.view.tabs.setTabEnabled(6, True) 
        else:  # Admin
            self.view.update_patient_button.setEnabled(True)
            self.view.delete_patient_button.setEnabled(True)
            self.view.tabs.setTabEnabled(2, True)
            self.view.tabs.setTabEnabled(3, True)
            self.view.tabs.setTabEnabled(4, True)
            self.view.tabs.setTabEnabled(5, True)
            self.view.tabs.setTabEnabled(6, True) 

    def handle_add_patient(self):
        if self.current_user_role:
            try:
                patient_data = self.view.get_patient_input()
                patient = Patient(
                    name=patient_data[0],
                    date_of_birth=patient_data[1],
                    gender=patient_data[2],
                    address=patient_data[3],
                    phone=patient_data[4],
                    admission_date=patient_data[5]
                )
                self.model.add_patient(patient)
            #     self.refresh_patient_list()
            #     self.view.clear_patient_inputs()
            #     self.view.show_message("Success", "Patient added")
            # except Exception as e:
            #     self.view.show_message("Error", str(e))
                if self.current_user_role in ["admin", "doctor"]:
                    self.refresh_patient_list()
                else:  # user
                    self.view.show_patient_table_with_one(patient)

                self.view.clear_patient_inputs()
                self.view.show_message("Success", "Patient added")
            except Exception as e:
                self.view.show_message("Error", str(e))




    def handle_update_patient(self):
        if (self.current_user_role == "admin" or self.current_user_role == "doctor") and self.selected_patient_id:
            try:
                patient_data = self.view.get_patient_input()
                patient = Patient(
                    patient_id=self.selected_patient_id,
                    name=patient_data[0],
                    date_of_birth=patient_data[1],
                    gender=patient_data[2],
                    address=patient_data[3],
                    phone=patient_data[4],
                    admission_date=patient_data[5]
                )
                self.model.update_patient(patient)
                self.refresh_patient_list()
                self.view.clear_patient_inputs()
                self.view.show_message("Success", "Patient updated")
            except Exception as e:
                self.view.show_message("Error", str(e))

    def handle_delete_patient(self):
        if self.current_user_role == "admin" and self.selected_patient_id:
            try:
                self.model.delete_patient(self.selected_patient_id)
                self.refresh_patient_list()
                self.view.clear_patient_inputs()
                self.view.show_message("Success", "Patient deleted")
            except Exception as e:
                self.view.show_message("Error", str(e))

    def handle_add_diagnosis(self):
        if (self.current_user_role == "admin" or self.current_user_role == "doctor") and self.selected_patient_id:
            try:
                icd_code, disease_name, diagnosis_date = self.view.get_diagnosis_input()
                diagnosis = Diagnosis(
                    patient_id=self.selected_patient_id,
                    icd_code=icd_code,
                    disease_name=disease_name,
                    diagnosis_date=diagnosis_date
                )
                self.model.add_diagnosis(diagnosis)
                self.refresh_diagnoses()
                self.view.clear_diagnosis_inputs()
                self.view.show_message("Success", "Diagnosis added")
            except Exception as e:
                self.view.show_message("Error", str(e))

    def handle_add_prescription(self):
        if (self.current_user_role == "admin" or self.current_user_role == "doctor") and self.selected_patient_id:
            try:
                medication, dosage, instructions, date, doctor_id = self.view.get_prescription_input()
                prescription = Prescription(
                    patient_id=self.selected_patient_id,
                    doctor_id=doctor_id,
                    medication_name=medication,
                    dosage=dosage,
                    instructions=instructions,
                    prescription_date=date
                )
                self.model.add_prescription(prescription)
                self.refresh_prescriptions()
                self.view.clear_prescription_inputs()
                self.view.show_message("Success", "Prescription added")
            except Exception as e:
                self.view.show_message("Error", str(e))

    def handle_add_visit(self):
        if (self.current_user_role == "admin" or self.current_user_role == "doctor") and self.selected_patient_id:
            try:
                visit_date, notes, doctor_id = self.view.get_visit_input()
                visit = Visit(
                    patient_id=self.selected_patient_id,
                    doctor_id=doctor_id,
                    visit_date=visit_date,
                    notes=notes
                )
                self.model.add_visit(visit)
                self.refresh_visits()
                self.view.clear_visit_inputs()
                self.view.show_message("Success", "Visit added")
            except Exception as e:
                self.view.show_message("Error", str(e))

    def handle_add_appointment(self):
        if (self.current_user_role == "admin" or self.current_user_role == "doctor") and self.selected_patient_id:
            try:
                appointment_date, status, doctor_id = self.view.get_appointment_input()
                appointment = Appointment(
                    patient_id=self.selected_patient_id,
                    doctor_id=doctor_id,
                    appointment_date=appointment_date,
                    status=status
                )
                self.model.add_appointment(appointment)
                self.refresh_appointments()
                self.view.clear_appointment_inputs()
                self.view.show_message("Success", "Appointment added")
            except Exception as e:
                self.view.show_message("Error", str(e))

    def handle_stats(self):
        stats = self.model.get_disease_stats()
        diagnoses, counts = zip(*stats) if stats else ([], [])
        plt.figure(figsize=(8, 6))
        plt.bar(diagnoses, counts)
        plt.xlabel("Disease")
        plt.ylabel("Number of Patients")
        plt.title("Patient Statistics by Diagnosis")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        # self.view.show_message("Statistics", "Chart saved as disease_stats.png")

    # def handle_stats_appointments(self):
    #     stats = self.model.get_appointment_stats()
    #     name, counts = zip(*stats) if stats else ([], [])
    #     plt.figure(figsize=(8, 6))
    #     plt.bar(name, counts)
    #     plt.xlabel("Doctor Name")
    #     plt.ylabel("Number of Appointments")
    #     plt.title("Appointment Statistics by Doctor")
    #     plt.xticks(rotation=45)
    #     plt.tight_layout()
    #     plt.show()

    def handle_stats_appointments(self):
        try:
            stats = self.model.get_appointment_stats()
            if not stats:
                self.view.show_message("Info", "No appointment statistics available")
                return
            
            # Unpack stats: expecting (doctor_id, name, count)
            _, names, counts = zip(*stats)  # Ignore doctor_id
            
            # Create bar chart
            plt.figure(figsize=(8, 6))
            plt.bar(names, counts, color='#0984e3')  # Match UI theme color
            plt.xlabel("Doctor Name")
            plt.ylabel("Number of Appointments")
            plt.title("Appointment Statistics by Doctor")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Save chart to file
            # chart_path = "appointment_stats.png"
            # plt.savefig(chart_path)
            # plt.close()  # Close figure to free memory
            
            plt.show()
            
        except Exception as e:
            self.view.show_message("Error", f"Failed to load appointment stats: {e}")

    def handle_patient_selection(self):
        selected = self.view.patient_table.selectedItems()
        if selected:
            row = self.view.patient_table.currentRow()
            self.selected_patient_id = int(self.view.patient_table.item(row, 0).text())
            patient_data = (
                self.view.patient_table.item(row, 1).text(),
                self.view.patient_table.item(row, 2).text(),
                self.view.patient_table.item(row, 3).text(),
                self.view.patient_table.item(row, 4).text(),
                self.view.patient_table.item(row, 5).text(),
                self.view.patient_table.item(row, 5).text() if self.view.patient_table.item(row, 5) else ""
            )
            self.view.set_selected_patient(self.selected_patient_id, *patient_data)
            self.refresh_diagnoses()
            self.refresh_prescriptions()
            self.refresh_visits()
            self.refresh_appointments()

    # def refresh_patient_list(self):
    #     patients = self.model.get_all_patients()
    #     self.view.display_patients(patients)
    #     self.selected_patient_id = None
    #     self.view.clear_diagnosis_inputs()
    #     self.view.clear_prescription_inputs()
    #     self.view.clear_visit_inputs()
    #     self.view.clear_appointment_inputs()
    def refresh_patient_list(self):
        patients = self.model.get_all_patients()
        self.view.display_patients([(p.id, p.name, p.date_of_birth, p.gender, p.address, p.phone, p.admission_date) for p in patients])
        self.selected_patient_id = None
        self.view.clear_diagnosis_inputs()
        self.view.clear_prescription_inputs()
        self.view.clear_visit_inputs()
        self.view.clear_appointment_inputs()

    # def refresh_doctor_list(self):
    #     doctors = self.model.get_doctors()
    #     self.view.populate_doctor_combo(doctors)

    def refresh_doctor_list(self):
        doctors = self.model.get_doctors()
        self.view.populate_doctor_combo(doctors)

    # def refresh_diagnoses(self):
    #     if self.selected_patient_id:
    #         diagnoses = self.model.get_diagnoses(self.selected_patient_id)
    #         self.view.display_diagnoses(diagnoses)
    #     else:
    #         self.view.display_diagnoses([])
    def refresh_diagnoses(self):
        if self.selected_patient_id:
            diagnoses = self.model.get_diagnoses(self.selected_patient_id)
            self.view.display_diagnoses([(d.id, d.icd_code, d.disease_name, d.diagnosis_date) for d in diagnoses])
        else:
            self.view.display_diagnoses([])

    def refresh_prescriptions(self):
        if self.selected_patient_id:
            prescriptions = self.model.get_prescriptions(self.selected_patient_id)
            self.view.display_prescriptions([(p.id, self.model.get_doctor_byid(p.doctor_id).name, p.medication_name, p.dosage, p.instructions, p.prescription_date) for p in prescriptions])
        else:
            self.view.display_prescriptions([])

    def refresh_visits(self):
        if self.selected_patient_id:
            visits = self.model.get_visits(self.selected_patient_id)
            self.view.display_visits([(v.id, self.model.get_doctor_byid(v.doctor_id).name, v.visit_date, v.notes) for v in visits])
        else:
            self.view.display_visits([])

    def refresh_appointments(self):
        if self.selected_patient_id:
            appointments = self.model.get_appointments(self.selected_patient_id)
            self.view.display_appointments([(a.id, self.model.get_doctor_byid(a.doctor_id).name, a.appointment_date, a.status) for a in appointments])
        else:
            self.view.display_appointments([])

# if __name__ == "__main__":
#     try:
#         app = QApplication(sys.argv)
#         print("hello")
#         model = DatabaseModel()
#         print("hello1")
#         view = HospitalView()
#         print("hello2")
#         controller = HospitalController(model, view)
#         print("hello3")
#         view.show()
#         sys.exit(app.exec_())
#     except Exception as e:
#         print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    from model import DatabaseModel

    print("hello")
    model = DatabaseModel()
    print("hello1")

    from PyQt5.QtWidgets import QApplication
    from view import HospitalView
    from controller import HospitalController

    app = QApplication(sys.argv)
    view = HospitalView()
    controller = HospitalController(model, view)
    view.show()
    sys.exit(app.exec_())

# admin - admin123
# doctor - doctor123