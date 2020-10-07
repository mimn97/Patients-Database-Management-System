
"""
This module contains the class AppointmentDatabase, which provides an
interface to an SQLite database containing information about appointments
in a hospital.

It is designed to be used for the REST API implementation in patients_api.py.
Note that this database is not real data.

Written by Minhwa (Mina) Lee
"""

import os
import sqlite3
from collections import OrderedDict


# Referenced from Professor Sommer's code
def row_to_dict_or_none(cur):
    """
    Given a cursor that has just been used to execute a query, try to fetch one
    row. If the there is no row to fetch, return None, otherwise return a
    dictionary representation of the row.

    :param cur: a cursor that has just been used to execute a query
    :return: a dict representation of the next row, or None
    """
    row = cur.fetchone()

    if row is None:
        return None
    else:
        return dict(row)


class AppointmentDatabase:
    """
    This class provides methods for getting and inserting information about
    appointments and other related information into an SQLite database.
    """

    def __init__(self, sqlite_filename):
        """
        Creates a connection to the database, and creates tables if the
        database file did not exist prior to object creation.

        :param sqlite_filename: the name of the SQLite database file
        """
        if os.path.isfile(sqlite_filename):
            create_tables = False
        else:
            create_tables = True

        self.conn = sqlite3.connect(sqlite_filename)
        self.conn.row_factory = sqlite3.Row

        cur = self.conn.cursor()
        cur.execute('PRAGMA foreign_keys = 1')
        cur.execute('PRAGMA journal_mode = WAL')
        cur.execute('PRAGMA synchronous = NORMAL')

        if create_tables:
            self.create_tables()

    def create_tables(self):
        """
        Create the tables for appointment information.
        """
        cur = self.conn.cursor()

        cur.execute('CREATE TABLE doctors(doctor_id INTEGER PRIMARY KEY, '
                    '    doctor TEXT UNIQUE)')

        cur.execute('CREATE TABLE symptoms(symptom_id INTEGER PRIMARY KEY, '
                    '      symptom TEXT UNIQUE)')

        cur.execute('CREATE TABLE patients(patient_id INTEGER PRIMARY KEY, '
                    '       FirstN TEXT UNIQUE , LastN TEXT UNIQUE, '
                    'gender TEXT, age INTEGER, birth text)')

        cur.execute('''CREATE TABLE app(app_id INTEGER PRIMARY KEY,
        patient_id INTEGER, doctor_id INTEGER, month TEXT, symptom_id INTEGER,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
        FOREIGN KEY (symptom_id) REFERENCES symptoms(symptom_id))
        ''')

        self.conn.commit()

    def insert_app(self, patient_first, patient_last, gender, age, birth,
                   doctor, month, symptom):
        """
        Inserts an appointment into the database.
        If any foreign key elements are not already in the database,
        then inserts those information.

        Returns a dictionary representation of the appointment.

        :param patient_first: first name of the patient of that appointment
        :param patient_last: last name of the patient of that appointment
        :param gender: gender of the patient
        :param age: age of the patient
        :param birth: birth of the patient
        :param doctor: the first name of doctor assigned to the appointment
        :param month: month of the appointment
        :param symptom: the name of symptom that the patient suffers from
        :return: a dictionary representation of the appointment.
        """

        cur = self.conn.cursor()

        self.insert_doctor(doctor)
        self.insert_symptoms(symptom)
        self.insert_patient(patient_first, patient_last, gender, age, birth)

        doctor_dict = self.get_doctor_by_name(doctor)
        doctor_id = doctor_dict['doctor_id']

        symp_dict = self.get_symptoms_by_name(symptom)
        symptom_id = symp_dict['symptom_id']

        patient_dict = self.get_patient_by_name(patient_first, patient_last)
        patient_id = patient_dict['patient_id']

        query = ('INSERT INTO app(patient_id, doctor_id, month, symptom_id)'
                 'VALUES(?, ?, ?, ?)')

        cur.execute(query, (patient_id, doctor_id, month, symptom_id))
        self.conn.commit()

        return self.get_app_by_id(cur.lastrowid)

    def get_app_by_id(self, app_id):
        """
        Provided an appointment's primary key, return a dictionary
        representation of the appointment, or None if there's no appointment
        with that primary key in the database.

        :param app_id: the primary key of the appointment
        :return: a dictionary of the patient
        """

        cur = self.conn.cursor()

        query = ('SELECT patients.FirstN as FirstN, patients.LastN as LastN,  '
                 'patients.gender as gender, patients.age as age, '
                 'patients.birth as birth, doctors.doctor as doctor, '
                 'app.month as month, app.app_id as app_id, '
                 'symptoms.symptom as symptom '
                 'FROM app, patients, doctors, symptoms '
                 'WHERE app.patient_id = patients.patient_id '
                 'AND app.doctor_id = doctors.doctor_id '
                 'AND app.symptom_id = symptoms.symptom_id '
                 'AND app.app_id = ?')

        cur.execute(query, (app_id,))
        return row_to_dict_or_none(cur)

    def get_all_apps(self):
        """
        Return a list dictionaries representing all of the appointments in
        the database.

        :return: a list of dict objects representing appointments
        """

        cur = self.conn.cursor()

        query = ('SELECT patients.FirstN as FirstN, patients.LastN as LastN, '
                 'patients.gender as gender, patients.age as age, '
                 'patients.birth as birth, doctors.doctor as doctor, '
                 'app.month as month, app.app_id as app_id, '
                 'symptoms.symptom as symptom '
                 'FROM app, patients, doctors, symptoms '
                 'WHERE app.patient_id = patients.patient_id '
                 'AND app.doctor_id = doctors.doctor_id '
                 'AND app.symptom_id = symptoms.symptom_id ')

        lst_apps = []
        cur.execute(query)

        for row in cur.fetchall():
            lst_apps.append(dict(row))

        return lst_apps

    def delete_app(self, app_id):
        """
        Delete the appointment with the given primary key.

        :param app_id: primary key of the appointment
        """

        cur = self.conn.cursor()

        query = 'DELETE FROM app WHERE app_id = ?'
        cur.execute(query, (app_id,))

        self.conn.commit()

    def insert_patient(self, patient_firstN, patient_lastN, gender, age,
                       birth):
        """
        Insert a patient into the database 'patient' if it does not exist.
        Do nothing if there is already a patient with the given first name
        and last name in the database.

        :param patient_firstN: first name of the patient
        :param patient_lastN: last name of the patient
        :param gender: gender of the patient
        :param age: age of the patient
        :param birth: birth of the patient
        :return: dict representing the patient
        """

        cur = self.conn.cursor()
        query = 'INSERT OR IGNORE INTO patients(FirstN, LastN, gender, age, ' \
                'birth) VALUES(?, ?, ?, ?, ?)'
        cur.execute(query, (patient_firstN, patient_lastN, gender, age, birth))
        self.conn.commit()
        return self.get_patient_by_name(patient_firstN, patient_lastN)

    def get_all_patients(self):
        """
        Get a list of dictionary representations of all the patients in the
        database.

        :return: list of dicts representing all patients
        """
        cur = self.conn.cursor()

        query = 'SELECT * FROM patients'

        lst_patients = []
        cur.execute(query)

        for row in cur.fetchall():
            lst_patients.append(dict(row))

        return lst_patients

    def get_patient_by_id(self, patient_id):
        """
        Get a dictionary representation of the patient with the given primary
        key. Return None if the patient does not exist.

        :param patient_id: primary key of the patient
        :return: a dictionary of the patient, or None
        """
        cur = self.conn.cursor()
        query = 'SELECT patient_id, FirstN, LastN, gender, age, birth ' \
                'FROM patients WHERE patient_id = ?'
        cur.execute(query, (patient_id,))
        return row_to_dict_or_none(cur)

    def get_patient_by_name(self, patient_firstN, patient_lastN):
        """
        Get a dictionary representation of the patient with the given first
        name and last name. Return None if the patient does not exist.

        :param patient_firstN: first name of the patient
        :param patient_lastN: first name of the patient
        :return: a dictionary of the patient, or None
        """
        cur = self.conn.cursor()
        query = 'SELECT patient_id, FirstN, LastN, gender, age, birth ' \
                'FROM patients WHERE FirstN = ? and LastN = ?'
        cur.execute(query, (patient_firstN, patient_lastN,))
        return row_to_dict_or_none(cur)

    def delete_patient(self, patient_id):
        """
        Delete the patient with the given primary id key.

        :param patient_id: primary key (id) of the patient

        """

        cur = self.conn.cursor()

        query1 = 'DELETE FROM app WHERE patient_id = ?'
        query2 = 'DELETE FROM patients WHERE patient_id = ?'

        cur.execute(query1, (patient_id,))
        cur.execute(query2, (patient_id,))

        self.conn.commit()

    def insert_doctor(self, doctor):
        """
        Insert a doctor into the database if it does not exist. Do nothing if
        there is already a doctor with the given name in the database.

        Return a dict representation of the doctor.

        :param  doctor: name of the doctor
        :return: dict representing the doctor
        """
        cur = self.conn.cursor()
        query = 'INSERT OR IGNORE INTO doctors(doctor) VALUES(?)'
        cur.execute(query, (doctor,))
        self.conn.commit()
        return self.get_doctor_by_name(doctor)

    def get_all_doctors(self):
        """
        Get a list of dictionary representations of all the doctors in the
        database.

        :return: list of dicts representing all doctors
        """
        cur = self.conn.cursor()

        query = 'SELECT * FROM doctors'

        lst_doctor = []
        cur.execute(query)

        for row in cur.fetchall():
            lst_doctor.append(dict(row))

        return lst_doctor

    def get_doctor_by_id(self, doctor_id):
        """
        Get a dictionary representation of the doctor with the given primary
        key. Return None if the doctor does not exist.

        :param doctor_id: primary key of the doctor
        :return: a dictionary of the doctor, or None
        """
        cur = self.conn.cursor()
        query = 'SELECT doctor_id, doctor FROM doctors WHERE doctor_id = ?'
        cur.execute(query, (doctor_id,))
        return row_to_dict_or_none(cur)

    def get_doctor_by_name(self, doctor):
        """
        Get a dictionary of the doctor with the given name.
        Return None when there is no such doctor in the database.

        :param doctor: name of the doctor
        :return: a dictionary representing the doctor, or None
        """
        cur = self.conn.cursor()
        query = 'SELECT doctor_id, doctor FROM doctors WHERE doctor = ?'
        cur.execute(query, (doctor,))
        return row_to_dict_or_none(cur)

    def delete_doctor(self, doctor_id):
        """
        Delete the doctor with the given primary id key.

        :param doctor_id: primary key (id) of the doctor

        """

        cur = self.conn.cursor()

        query1 = 'DELETE FROM app WHERE doctor_id = ?'
        query2 = 'DELETE FROM doctors WHERE doctor_id = ?'

        cur.execute(query1, (doctor_id,))
        cur.execute(query2, (doctor_id,))

        self.conn.commit()

    def insert_symptoms(self, symptom):
        """
        Insert a symptom case into the database only if it doesn't exist.
        Return a dictionary representation of the symptom.

        :param symptom: name of the symptom
        :return: dictionary representing the symptom
        """

        cur = self.conn.cursor()
        query = 'INSERT OR IGNORE INTO symptoms(symptom) VALUES(?)'
        cur.execute(query, (symptom,))
        self.conn.commit()
        return self.get_symptoms_by_name(symptom)

    def get_all_symptoms(self):
        """
        Get a list of dictionary representation of all the symptoms in the
        database.
        :return: list of dictionaries representing all symptoms.
        """
        cur = self.conn.cursor()
        query = 'SELECT * FROM symptoms'

        lst_symptoms = []
        cur.execute(query)

        for row in cur.fetchall():
            lst_symptoms.append(dict(row))

        return lst_symptoms

    def get_symptoms_by_id(self, symptom_id):
        """
        Get a dictionary representation of the symptom provided with the given
        key. Return nothing if the symptom is not in the database.

        :param symptom_id: primary key of the symptom
        :return: a dictionary of that symptom, or None.
        """

        cur = self.conn.cursor()
        query = 'SELECT symptom_id, symptom FROM symptoms WHERE symptom_id = ?'
        cur.execute(query, (symptom_id,))
        return row_to_dict_or_none(cur)

    def get_symptoms_by_name(self, symptom):
        """
        Get a dictionary representation of the symptom with the provided name,
        or it returns none if there's no such symptom in the database.

        :param symptom: name of the symptom
        :return: a dictionary of that symptom, or None.
        """

        cur = self.conn.cursor()
        query = 'SELECT symptom_id, symptom FROM symptoms WHERE symptom = ?'
        cur.execute(query, (symptom,))
        return row_to_dict_or_none(cur)

    def delete_symptom(self, symptom_id):
        """
        Delete the symptom with the given primary key.

        :param symptom_id: primary key of the symptom
        """

        cur = self.conn.cursor()

        query1 = 'DELETE FROM app WHERE symptom_id = ?'
        query2 = 'DELETE FROM symptoms WHERE symptom_id = ?'

        cur.execute(query1, (symptom_id,))
        cur.execute(query2, (symptom_id,))

        self.conn.commit()


if __name__ == '__main__':
    db = AppointmentDatabase('appointments.sqlite')

    db.insert_app('Mina', 'Lee', 'Female', 22, '1997-11-21', 'Amy',
                  'April', 'Headache')
    db.insert_app('Danny', 'Park', 'Male', 21, '1999-04-22', 'Robert',
                  'March', 'Knee sprain')
    db.insert_app('Grace', 'Kim', 'Female', 21, '1999-01-02', 'Nathan',
                  'April', 'Stomachache')
    db.insert_app('Victoria', 'Choi', 'Female', 18, '2002-10-08', 'Claire',
                  'March', 'Mental clinic')
    db.insert_app('Alex', 'Hwang', 'Male', 27, '1993-09-16', 'Mary',
                  'May', 'Waist pain')
    db.insert_app('Stacey', 'Parker', 'Female', 21, '1998-09-12', 'Amy',
                  'April', 'Headache')
    db.insert_app('Joon', 'Brandon', 'Male', 53, '1967-05-12', 'Robert',
                  'March', 'Knee sprain')

    doctors = db.get_all_doctors()
    print('List of all doctors: ', doctors)

    patients = db.get_all_patients()
    print('List of all patients: ', patients)

    symptoms = db.get_all_symptoms()
    print('List of all symptoms: ', symptoms)

    apps = db.get_all_apps()
    print('List of all appointments: ', apps)
