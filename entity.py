import hashlib
from datetime import datetime

# Entity Classes
class User:
    def __init__(self, username, password, role, user_id=None):
        self.id = user_id
        self.username = username
        self.password = self._hash_password(password)
        self.role = role

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate(self):
        if not self.username or not self.password or not self.role:
            raise ValueError("Username, password, and role are required")
        if self.role not in ["admin", "user", "doctor"]:
            raise ValueError("Invalid role")

class Patient:
    def __init__(self, name, date_of_birth, gender, address, phone, admission_date, patient_id=None):
        self.id = patient_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.address = address
        self.phone = phone
        self.admission_date = admission_date

    def validate(self):
        if not self.name or not self.date_of_birth:
            raise ValueError("Name and date of birth are required")
        if self.gender not in ["Male", "Female", "Other"]:
            raise ValueError("Invalid gender")

class Diagnosis:
    def __init__(self, patient_id, icd_code, disease_name, diagnosis_date, diagnosis_id=None):
        self.id = diagnosis_id
        self.patient_id = patient_id
        self.icd_code = icd_code
        self.disease_name = disease_name
        self.diagnosis_date = diagnosis_date

    def validate(self):
        if not self.patient_id or not self.disease_name:
            raise ValueError("Patient ID and disease name are required")

# Add similar classes for Prescription, Visit, Appointment, and Doctor
class Prescription:
    def __init__(self, patient_id, doctor_id, medication_name, dosage, instructions, prescription_date, prescription_id=None):
        self.id = prescription_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.medication_name = medication_name
        self.dosage = dosage
        self.instructions = instructions
        self.prescription_date = prescription_date

    def validate(self):
        if not all([self.patient_id, self.doctor_id, self.medication_name, self.dosage]):
            raise ValueError("Patient ID, doctor ID, medication name, and dosage are required")

class Visit:
    def __init__(self, patient_id, doctor_id, visit_date, notes, visit_id=None):
        self.id = visit_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.visit_date = visit_date
        self.notes = notes

    def validate(self):
        if not all([self.patient_id, self.doctor_id]):
            raise ValueError("Patient ID and doctor ID are required")

class Appointment:
    def __init__(self, patient_id, doctor_id, appointment_date, status, appointment_id=None):
        self.id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.status = status

    def validate(self):
        if not all([self.patient_id, self.doctor_id, self.status]):
            raise ValueError("Patient ID, doctor ID, and status are required")
        if self.status not in ["Scheduled", "Cancelled", "Completed"]:
            raise ValueError("Invalid status")

class Doctor:
    def __init__(self, name, specialty, phone, user_id= None, doctor_id=None):
        self.id = doctor_id
        self.name = name
        self.specialty = specialty
        self.phone = phone
        self.user_id = user_id

    def validate(self):
        if not self.name:
            raise ValueError("Doctor name is required")