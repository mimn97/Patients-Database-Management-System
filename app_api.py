"""
This is a Flask application that provides an API for accessing and
modifying the data in the database 'appointments.sqlite.'
You can get, post, and delete data about appointments, patients, doctors, and
symptoms in each requests through terminal.

Written by Minhwa (Mina) Lee
"""

from flask import Flask, g, jsonify, request, render_template
from flask.views import MethodView
import os
import sqlite3
from app_db import AppointmentDatabase
from collections import OrderedDict

app = Flask(__name__)

app.config['DATABASE'] = os.path.join(app.root_path, 'appointments.sqlite')


#  Referenced from Professor Sommer's Code
def connect_db():
    """
    Returns a sqlite connection object associated with the application's
    database file.
    """

    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row

    return conn


#  Referenced from Professor Sommer's Code
def get_db():
    """
    Returns a AppointmentDatabase instance for accessing the database.
    If the database file does not yet exist, it creates a new database.
    """

    if not hasattr(g, 'app_db'):
        g.apps_db = AppointmentDatabase(app.config['DATABASE'])

    return g.apps_db


#  Referenced from Professor Sommer's Code
class RequestError(Exception):

    def __init__(self, status_code, error_message):
        # Call the super class's initializer. Unlike in C++, this does not
        # happen automatically in Python.
        super().__init__(self)

        self.status_code = str(status_code)
        self.error_message = error_message

    def to_response(self):
        """
        Create a Response object containing the error message as JSON.

        :return: the response
        """

        response = jsonify({'error': self.error_message})
        response.status = self.status_code
        return response


#  Referenced from Professor Sommer's Code
@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    """
    Returns a JSON response built from a RequestError.

    :param error: the RequestError
    :return: a response containing the error message
    """
    return error.to_response()


class AppointmentsView(MethodView):
    """
    This view handles all the /apps requests.
    """

    def get(self, app_id):
        """
        Handle GET requests.

        Returns JSON representing all of the appointments
        if app_id is None, or a single appointment if app_id exists.

        :param app_id: id of an appointment, or None for all appointments
        :return: JSON response
        """
        if app_id is None:
            all_apps = get_db().get_all_apps()
            return jsonify(all_apps)
        else:
            appointment = get_db().get_app_by_id(app_id)

            if app is not None:
                response = jsonify(appointment)
            else:
                raise RequestError(404, 'appointment not found')

            return response

    def post(self):
        """
        Implements POST /apps

        Requires the form parameters 'FirstN', 'LastN', 'gender', 'age',
        'birth', 'doctor FirstN', 'month', and 'Symptom'.

        :return: JSON response representing the new appointment's information
        """

        for parameter in ('FirstN', 'LastN', 'gender', 'age', 'birth',
                          'doctor', 'month', 'symptom'):
            if parameter not in request.form:
                error = 'parameter {} required'.format(parameter)
                raise RequestError(422, error)

        response = jsonify(get_db().insert_app(request.form['FirstN'],
                                               request.form['LastN'],
                                               request.form['gender'],
                                               request.form['age'],
                                               request.form['birth'],
                                               request.form['doctor'],
                                               request.form['month'],
                                               request.form['symptom']))

        return response

    def delete(self, app_id):
        """
        Handle DELETE requests. The app_id must be provided.

        :param app_id: id of an appointment
        :return: JSON response containing a message
        """
        if get_db().get_app_by_id(app_id) is None:
            raise RequestError(404, 'appointment not found')

        get_db().delete_app(app_id)

        return jsonify({'message': 'appointment deleted successfully'})


class DoctorsView(MethodView):
    """
    This view handles all the /doctors requests.
    """

    def get(self, doctor_id):
        """
        Handle GET requests.

        Returns JSON representing all of the doctors if doctor_id is None,
        or just one doctor if doctor_id exists.

        :param doctor_id: id of a doctor, or None for all doctors
        :return: JSON response
        """
        if doctor_id is None:
            all_doctors = get_db().get_all_doctors()
            return jsonify(all_doctors)
        else:
            doctor = get_db().get_doctor_by_id(doctor_id)

            if doctor is not None:
                response = jsonify(doctor)
            else:
                raise RequestError(404, 'doctor not found')

            return response

    def post(self):
        """
        Handles a POST request to insert a new doctor. Returns a JSON
        response representing the new doctor.

        Requires the form parameter 'doctor'

        :return: a response containing the JSON representation of the doctor
        """
        if 'doctor' not in request.form:
            raise RequestError(422, 'doctor first name required')
        else:
            response = jsonify(get_db().insert_doctor(request.form['doctor']))

        return response

    def delete(self, doctor_id):
        """
        Handle DELETE requests. The doctor_id must be provided.

        :param doctor_id: id of a doctor
        :return: JSON response containing a message
        """
        if get_db().get_doctor_by_id(doctor_id) is None:
            raise RequestError(404, 'doctor not found')

        get_db().delete_doctor(doctor_id)

        return jsonify({'message': 'doctor deleted successfully'})


class PatientsView(MethodView):
    """
    This view handles all the /patients requests.
    """

    def get(self, patient_id):
        """
        Handle GET requests.

        Returns JSON representing all of the patients
        if patient_id is None, or just one patient if patient_id exists.

        :param patient_id:  id of a patient, or None for
        all patients
        :return: JSON response
        """
        if patient_id is None:
            return jsonify(get_db().get_all_patients())
        else:
            patient = get_db().get_patient_by_id(patient_id)

            if patient is not None:
                response = jsonify(patient)
            else:
                raise RequestError(404, 'patient not found')

            return response

    def post(self):
        """
        Handles a POST request to insert a new patient. Returns a JSON
        response representing the new patient.

        Requires the form parameter 'FirstN', 'LastN', 'gender', 'age',
        'birth'

        :return: a response containing the JSON representation of
        the appointment
        """
        for parameter in ('FirstN', 'LastN', 'gender', 'age', 'birth'):
            if parameter not in request.form:
                error = 'parameter {} required'.format(parameter)
                raise RequestError(422, error)

        else:
            response = jsonify(get_db().insert_patient(request.form['FirstN'],
                                                       request.form['LastN'],
                                                       request.form['gender'],
                                                       request.form['age'],
                                                       request.form['birth']))
        return response

    def delete(self, patient_id):
        """
        Handle DELETE requests. The patient_id must be provided.

        :param patient_id: id of a patient
        :return: JSON response containing a message
        """
        if get_db().get_patient_by_id(patient_id) is None:
            raise RequestError(404, 'patient not found')

        get_db().delete_patient(patient_id)

        return jsonify({'message': 'patient deleted successfully'})


class SymptomsView(MethodView):
    """
    This view handles all the /symptoms requests.
    """

    def get(self, symptom_id):
        """
        Handle GET requests.

        Returns JSON representing all of the symptoms if symptom_id is None,
        or just one symptom if symptom_id exists.

        :param symptom_id: id of a symptom, or None for all symptoms
        :return: JSON response
        """
        if symptom_id is None:
            return jsonify(get_db().get_all_symptoms())
        else:
            symptom = get_db().get_symptoms_by_id(symptom_id)

            if symptom is not None:
                response = jsonify(symptom)
            else:
                raise RequestError(404, 'symptom not found')

            return response

    def post(self):
        """
        Handles a POST request to insert a new symptom. Returns a JSON
        response representing the new symptom.

        Requires the form parameter 'symptom'

        :return: a response containing the JSON representation of the symptom
        """
        if 'symptom' not in request.form:
            raise RequestError(422, 'symptom name required')
        else:
            response = jsonify(get_db().insert_symptoms
                               (request.form['symptom']))

        return response

    def delete(self, symptom_id):
        """
        Handle DELETE requests. The symptom_id must be provided.

        :param symptom_id: id of a symptom
        :return: JSON response containing a message
        """
        if get_db().get_symptoms_by_id(symptom_id) is None:
            raise RequestError(404, 'symptom not found')

        get_db().delete_symptom(symptom_id)

        return jsonify({'message': 'symptom deleted successfully'})


# For API Views

# Register AppointmentsView as the handler for all the /apps requests.
apps_view = AppointmentsView.as_view('app_view')
app.add_url_rule('/apps', defaults={'app_id': None},
                 view_func=apps_view, methods=['GET'])
app.add_url_rule('/apps', view_func=apps_view, methods=['POST'])
app.add_url_rule('/apps/<int:app_id>', view_func=apps_view,
                 methods=['GET', 'DELETE'])

# Register DoctorsView as the handler for all the /doctors requests
doctors_view = DoctorsView.as_view('doctors_view')
app.add_url_rule('/doctors', defaults={'doctor_id': None},
                 view_func=doctors_view, methods=['GET'])
app.add_url_rule('/doctors', view_func=doctors_view, methods=['POST'])
app.add_url_rule('/doctors/<int:doctor_id>', view_func=doctors_view,
                 methods=['GET', 'DELETE'])

# Register PatientsView as the handler for all the /patients requests
patients_view = PatientsView.as_view('patients_view')
app.add_url_rule('/patients', defaults={'patient_id': None},
                 view_func=patients_view, methods=['GET'])
app.add_url_rule('/patients', view_func=patients_view, methods=['POST'])
app.add_url_rule('/patients/<int:patient_id>', view_func=patients_view,
                 methods=['GET', 'DELETE'])

# Register SymptomsView as the handler for all the /symptoms requests
symptoms_view = SymptomsView.as_view('symptoms_view')
app.add_url_rule('/symptoms', defaults={'symptom_id': None},
                 view_func=symptoms_view, methods=['GET'])
app.add_url_rule('/symptoms', view_func=symptoms_view, methods=['POST'])
app.add_url_rule('/symptoms/<int:symptom_id>', view_func=symptoms_view,
                 methods=['GET', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
