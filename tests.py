"""
This file includes all pytest tests that demonstrate the correctness of codes
used in the all functions of the class 'AppointmentDataBase.'

Written by Minhwa (Mina) Lee
"""

from app_db import AppointmentDatabase


def build_db_path(directory):
    return directory / 'test.sqlite'


def test_initializer(tmp_path):
    AppointmentDatabase(build_db_path(tmp_path))


def test_insert_app(tmp_path):
    """
    Test that insert_app() runs without raising exceptions, and correctly
    returns a dictionary representing the new appointment.
    """
    db = AppointmentDatabase(build_db_path(tmp_path))

    app = db.insert_app('Mina', 'Lee', 'Female', 22, '1997-11-21', 'Amy',
                        'April', 'Headache')

    assert app['FirstN'] == 'Mina'
    assert app['LastN'] == 'Lee'
    assert app['gender'] == 'Female'
    assert app['age'] == 22
    assert app['birth'] == '1997-11-21'
    assert app['doctor'] == 'Amy'
    assert app['month'] == 'April'
    assert app['symptom'] == 'Headache'


def test_get_app_by_id(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_app_by_id(1) is None

    app_inserted = db.insert_app('Mina', 'Kim', 'Female', 22, '1997-11-21',
                                 'David', 'April', 'Cold')
    app = db.get_app_by_id(1)

    assert app_inserted == app

    assert db.get_app_by_id(2) is None

    app_inserted = db.insert_app('Danny', 'Park', 'Male', 21, '1999-04-22',
                                 'Emily', 'March', 'Diarrhea')
    app = db.get_app_by_id(2)

    assert app_inserted == app


def test_get_all_apps(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_all_apps() == []

    app_inserted = db.insert_app('Mina', 'Lee', 'Female', 22, '1997-11-21',
                                 'David', 'April', 'Cold')

    apps_inserted = [app_inserted]

    apps = db.get_all_apps()

    assert len(apps) == 1
    assert apps[0] == app_inserted

    apps_inserted.append(db.insert_app('Victoria', 'Kim', 'Female', 18,
                                       '2002-10-08', 'Claire',
                                       'May', 'Mental clinic'))

    apps = db.get_all_apps()

    assert len(apps) == 2

    for app in apps_inserted:
        assert app in apps


def test_delete_app(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))
    app_inserted = db.insert_app('Anna', 'Kim', 'Female', 22,
                                         '1997-10-21', 'Roger', 'April',
                                 'COVID-19')
    apps = db.get_all_apps()

    assert len(apps) == 1
    assert apps[0] == app_inserted

    apps = db.delete_app(1)
    assert apps is None


def test_insert_doctor(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    doctor = db.insert_doctor('John')
    assert doctor['doctor'] == 'John'


def test_get_all_doctors(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_all_doctors() == []

    doctor_inserted = db.insert_doctor('Molly')
    doctors_inserted = [doctor_inserted]

    doctors = db.get_all_doctors()

    assert len(doctors) == 1
    assert doctors[0] == doctor_inserted

    doctors_inserted.append(db.insert_doctor('Jill'))
    doctors = db.get_all_doctors()

    assert len(doctors) == 2

    for doctor in doctors_inserted:
        assert doctor in doctors


def test_get_doctor_by_id(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_doctor_by_id(1) is None

    doctor_inserted = db.insert_doctor('Rachel')
    doctor = db.get_doctor_by_id(1)
    assert doctor_inserted == doctor

    assert db.get_doctor_by_id(2) is None

    doctor_inserted = db.insert_doctor('Kelly')
    doctor = db.get_doctor_by_id(2)
    assert doctor_inserted == doctor


def test_get_doctor_by_name(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_doctor_by_name('Rachel') is None

    doctor_inserted = db.insert_doctor('Rachel')
    doctor = db.get_doctor_by_name('Rachel')
    assert doctor_inserted == doctor

    assert db.get_doctor_by_name('Robert') is None

    doctor_inserted = db.insert_doctor('Robert')
    doctor = db.get_doctor_by_name('Robert')
    assert doctor_inserted == doctor


def test_delete_doctor(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    doctor_inserted = db.insert_doctor('Amy')
    doctors = db.get_all_doctors()

    assert len(doctors) == 1
    assert doctors[0] == doctor_inserted

    doctors = db.delete_doctor(1)
    assert doctors is None


def test_insert_patients(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    patient = db.insert_patient('Mina', 'Lee', 'Female', 22, '1997-11-21')
    assert patient['FirstN'] == 'Mina'
    assert patient['LastN'] == 'Lee'
    assert patient['gender'] == 'Female'
    assert patient['age'] == 22
    assert patient['birth'] == '1997-11-21'


def test_get_all_patients(tmp_path):

    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_all_patients() == []

    patient_inserted = db.insert_patient('Mina', 'Lee', 'Female', 22,
                                         '1997-11-21')
    patients_inserted = [patient_inserted]

    patients = db.get_all_patients()

    assert len(patients) == 1
    assert patients[0] == patient_inserted

    patients_inserted.append(db.insert_patient('Danny', 'Park', 'Male', 21,
                                               '1999-04-22'))
    patients = db.get_all_patients()

    assert len(patients) == 2

    for patient in patients_inserted:
        assert patient in patients


def test_get_patient_by_id(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_patient_by_id(1) is None

    patient_inserted = db.insert_patient('Mina', 'Lee', 'Female', 22,
                                         '1997-11-21')
    patient = db.get_patient_by_id(1)
    assert patient_inserted == patient

    assert db.get_patient_by_id(2) is None

    patient_inserted = db.insert_patient('Danny', 'Park', 'Male', 21,
                                         '1999-04-22')
    patient = db.get_patient_by_id(2)
    assert patient_inserted == patient


def test_get_patient_by_name(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_patient_by_name('Mina', 'Lee') is None

    patient_inserted = db.insert_patient('Mina', 'Lee', 'Female', 22,
                                         '1997-11-21')
    patient = db.get_patient_by_name('Mina', 'Lee')
    assert patient_inserted == patient

    assert db.get_patient_by_name('Danny', 'Park') is None

    patient_inserted = db.insert_patient('Danny', 'Park', 'Male', 21,
                                         '1999-04-22')
    patient = db.get_patient_by_name('Danny', 'Park')
    assert patient_inserted == patient


def test_delete_apps(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    patient_inserted = db.insert_patient('Mina', 'Lee', 'Female', 22,
                                         '1997-11-21')
    patients = db.get_all_patients()

    assert len(patients) == 1
    assert patients[0] == patient_inserted

    patients = db.delete_patient(1)
    assert patients is None


def test_insert_symptoms(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    symptom = db.insert_symptoms('Flu')
    assert symptom['symptom'] == 'Flu'


def test_get_all_symptoms(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_all_symptoms() == []

    symptom_inserted = db.insert_symptoms('Sore throat')
    symptoms_inserted = [symptom_inserted]

    symptoms = db.get_all_symptoms()

    assert len(symptoms) == 1
    assert symptoms[0] == symptom_inserted

    symptoms_inserted.append(db.insert_symptoms('Headache'))
    symptoms = db.get_all_symptoms()

    assert len(symptoms) == 2

    for symptom in symptoms_inserted:
        assert symptom in symptoms


def test_get_symptom_by_id(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_symptoms_by_id(1) is None

    symptom_inserted = db.insert_symptoms('Stomachache')
    symptom = db.get_symptoms_by_id(1)
    assert symptom_inserted == symptom

    assert db.get_symptoms_by_id(2) is None

    symptom_inserted = db.insert_symptoms('Diarrhea')
    symptom = db.get_symptoms_by_id(2)
    assert symptom_inserted == symptom


def test_get_symptom_by_name(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    assert db.get_symptoms_by_name('Stomachache') is None

    symptom_inserted = db.insert_symptoms('Stomachache')
    symptom = db.get_symptoms_by_name('Stomachache')
    assert symptom_inserted == symptom

    assert db.get_symptoms_by_name('COVID-19') is None

    symptom_inserted = db.insert_symptoms('COVID-19')
    symptom = db.get_symptoms_by_name('COVID-19')
    assert symptom_inserted == symptom


def test_delete_symptom(tmp_path):
    db = AppointmentDatabase(build_db_path(tmp_path))

    symptom_inserted = db.insert_symptoms('Wrist pain')
    symptoms = db.get_all_symptoms()

    assert len(symptoms) == 1
    assert symptoms[0] == symptom_inserted

    symptoms = db.delete_symptom(1)
    assert symptoms is None
