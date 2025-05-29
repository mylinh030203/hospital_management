import mysql.connector
import hashlib
import os
import requests
from entity import User, Patient, Appointment, Visit, Diagnosis, Prescription, Doctor

class DatabaseModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="linhptm",
                password="Havana18081988@",
                database="hospital_db"
            )
            print("success")
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            raise
        except Exception as e:
            print(f"Other Error: {e}")
            raise


    def register_user(self, user: User, doctor: Doctor = None):
        user.validate()
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (user.username, user.password, user.role))
        user_id = self.get_user_by_username(user.username)
        if user.role == "doctor":
            if doctor is None:
                raise ValueError("Doctor information is required for doctor role.")
            doctor.user_id = user_id
            doctor.validate()
            query = "INSERT INTO doctors (name, specialty, phone, user_id) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (doctor.name, doctor.specialty, doctor.phone, doctor.user_id))
    
        self.connection.commit()
        return self.cursor.lastrowid

    def authenticate_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = "SELECT role FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, hashed_password))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_patient(self, patient: Patient):
        patient.validate()
        query = """INSERT INTO patients (name, date_of_birth, gender, address, phone, admission_date)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(query, (
            patient.name, patient.date_of_birth, patient.gender,
            patient.address, patient.phone, patient.admission_date
        ))
        self.connection.commit()
        return self.cursor.lastrowid
    def get_user_by_username(self, username):
        query = "SELECT id FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return None

    def update_patient(self, patient: Patient):
        patient.validate()
        query = """UPDATE patients SET name=%s, date_of_birth=%s, gender=%s, address=%s, phone=%s,
                   admission_date=%s WHERE id=%s"""
        self.cursor.execute(query, (
            patient.name, patient.date_of_birth, patient.gender,
            patient.address, patient.phone, patient.admission_date, patient.id
        ))
        self.connection.commit()

    def delete_patient(self, patient_id):
        query = "DELETE FROM patients WHERE id=%s"
        self.cursor.execute(query, (patient_id,))
        self.connection.commit()

    def get_all_patients(self):
        query = "SELECT * FROM patients"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [Patient(
            patient_id=row[0], name=row[1], date_of_birth=row[2],
            gender=row[3], address=row[4], phone=row[5], admission_date=row[6]
        ) for row in rows]

    def add_diagnosis(self, diagnosis: Diagnosis):
        diagnosis.validate()
        query = """INSERT INTO diagnoses (patient_id, icd_code, disease_name, diagnosis_date)
                   VALUES (%s, %s, %s, %s)"""
        self.cursor.execute(query, (
            diagnosis.patient_id, diagnosis.icd_code,
            diagnosis.disease_name, diagnosis.diagnosis_date
        ))
        self.connection.commit()

    def get_diagnoses(self, patient_id):
        query = "SELECT * FROM diagnoses WHERE patient_id = %s"
        self.cursor.execute(query, (patient_id,))
        rows = self.cursor.fetchall()
        return [Diagnosis(
            diagnosis_id=row[0], patient_id=row[1], icd_code=row[2],
            disease_name=row[3], diagnosis_date=row[4]
        ) for row in rows]

    def add_prescription(self, prescription: Prescription):
        prescription.validate()
        query = """INSERT INTO prescriptions (patient_id, doctor_id, medication_name, dosage, instructions, prescription_date)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(query, (
            prescription.patient_id, prescription.doctor_id, prescription.medication_name,
            prescription.dosage, prescription.instructions, prescription.prescription_date
        ))
        self.connection.commit()

    def get_prescriptions(self, patient_id):
        query = "SELECT * FROM prescriptions WHERE patient_id = %s"
        self.cursor.execute(query, (patient_id,))
        rows = self.cursor.fetchall()
        return [Prescription(
            prescription_id=row[0], patient_id=row[1], doctor_id=row[2],
            medication_name=row[3], dosage=row[4], instructions=row[5], prescription_date=row[6]
        ) for row in rows]

    def add_visit(self, visit: Visit):
        visit.validate()
        query = """INSERT INTO visits (patient_id, doctor_id, visit_date, notes)
                   VALUES (%s, %s, %s, %s)"""
        self.cursor.execute(query, (
            visit.patient_id, visit.doctor_id, visit.visit_date, visit.notes
        ))
        self.connection.commit()

    def get_visits(self, patient_id):
        query = "SELECT * FROM visits WHERE patient_id = %s"
        self.cursor.execute(query, (patient_id,))
        rows = self.cursor.fetchall()
        return [Visit(
            visit_id=row[0], patient_id=row[1], doctor_id=row[2],
            visit_date=row[3], notes=row[4]
        ) for row in rows]

    def add_appointment(self, appointment: Appointment):
        appointment.validate()
        query = """INSERT INTO appointments (patient_id, doctor_id, appointment_date, status)
                   VALUES (%s, %s, %s, %s)"""
        self.cursor.execute(query, (
            appointment.patient_id, appointment.doctor_id,
            appointment.appointment_date, appointment.status
        ))
        self.connection.commit()

    def get_appointments(self, patient_id):
        query = "SELECT * FROM appointments WHERE patient_id = %s"
        self.cursor.execute(query, (patient_id,))
        rows = self.cursor.fetchall()
        return [Appointment(
            appointment_id=row[0], patient_id=row[1], doctor_id=row[2],
            appointment_date=row[3], status=row[4]
        ) for row in rows]

    def get_doctors(self):
        query = "SELECT * FROM doctors"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [Doctor(doctor_id=row[0], name=row[1], specialty=row[2], phone=row[3]) for row in rows]
    
    
    def get_doctor_byid(self, doctor_id):
        query = "SELECT * FROM doctors WHERE id = %s"
        self.cursor.execute(query, (doctor_id,))
        row = self.cursor.fetchone()
        return Doctor(doctor_id=row[0], name=row[1], specialty=row[2], phone=row[3])

    def get_disease_stats(self):
        query = "SELECT disease_name, COUNT(*) FROM diagnoses GROUP BY disease_name"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_appointment_stats(self):
        query = "SELECT a.doctor_id, d.name, COUNT(*) FROM appointments a JOIN doctors d ON a.doctor_id = d.id GROUP BY a.doctor_id, d.name"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_icd_code(self, search_term):
        try:
            url = f"https://icd10api.com/?code={search_term}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching ICD code: {e}")
            return []

    def close(self):
        self.cursor.close()
        self.connection.close()