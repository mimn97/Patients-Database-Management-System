"""
A Flask application in a HTML form to access information in the database.
This also adds new appointment to the database.
(as an additional feature for the project)

Written by Minhwa (Mina) Lee
"""


from flask import Flask, g, jsonify, request, render_template
from flask.views import MethodView
import os
from app_db import AppointmentDatabase
from collections import OrderedDict

app = Flask(__name__)

app.config['DATABASE'] = os.path.join(app.root_path, 'appointments.sqlite')


#  Referenced from Professor Sommer's Code
def get_db():
    """
    Returns a AppointmentDatabase instance for accessing the database.
    If the database file does not yet exist, it creates a new database.
    """

    if not hasattr(g, 'app_db'):
        g.apps_db = AppointmentDatabase(app.config['DATABASE'])

    return g.apps_db

# Referenced from Professor Sommer's code
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


def get_app_by_doctor():
    """
     Returns a dictionary containing appointments indexed by doctor.
     The dictionary keys are doctor names, and the values are lists of
     appointments.
     Each appointment is represented by a sqlite row object,
     which can be used like a dictionary.
    """

    cur = get_db().conn.cursor()

    # By using an OrderedDict we will preserve alphabetical order of
    # doctors

    app_by_doctor = OrderedDict()

    query = '''
    SELECT doctors.doctor as doctor, patients.FirstN as FirstN,
    patients.LastN as LastN, patients.gender as gender, patients.age as age,
    patients.birth as birth, app.month as month, symptoms.symptom as symptom
    FROM doctors, patients, app, symptoms
    WHERE app.doctor_id = doctors.doctor_id
    AND app.patient_id = patients.patient_id
    AND app.symptom_id = symptoms.symptom_id
    ORDER BY doctor, FirstN'''

    for row in cur.execute(query):
        doctor = row['doctor']

        if doctor not in app_by_doctor:
            app_by_doctor[doctor] = []

        app_by_doctor[doctor].append(row)

    return app_by_doctor


def get_app_by_month():
    """
    Returns a dictionary containing appointments indexed by month.
    The dictionary keys are month names, and the values are lists of
    appointments.
    Each appointment is represented by a sqlite row object,
    which can be used like a dictionary.
    """

    cur = get_db().conn.cursor()

    # By using an OrderedDict we will preserve alphabetical order of month
    app_by_month = OrderedDict()

    query = '''
    SELECT app.month as month, patients.FirstN as FirstN, patients.LastN as
    LastN, patients.gender as gender, patients.age as age,
    patients.birth as birth,
    doctors.doctor as doctor, symptoms.symptom as symptom
    FROM doctors, patients, app, symptoms
    WHERE app.doctor_id = doctors.doctor_id
    AND app.patient_id = patients.patient_id
    AND app.symptom_id = symptoms.symptom_id
    ORDER BY month, FirstN'''

    for row in cur.execute(query):
        month = row['month']

        if month not in app_by_month:
            app_by_month[month] = []

        app_by_month[month].append(row)

    return app_by_month


class MainView(MethodView):
    """
    Handles the main page for the website.
    """

    def get(self):
        """
        Serves the main webpage for the API.
        """
        return render_template("main.html")


class AppsView(MethodView):
    """
    Handles the page for the appointment
    """

    def get(self):
        """
        Serves a page which shows all the appointments in the database.
        """
        return render_template("appointments.html",
                               apps=get_db().get_all_apps())


class DoctorsView(MethodView):
    """
    Handles the page for doctors
    """

    def get(self):
        """
        Serves a page which shows all doctors in the database.
        """
        return render_template("doctors.html",
                               doctors=get_db().get_all_doctors())


class PatientsView(MethodView):
    """
    Handles the page for the patients.
    """

    def get(self):
        """
        Serves the page for showing all patients in the database.
        """
        return render_template("patients.html",
                               patients=get_db().get_all_patients())


class SymptomsView(MethodView):
    """
    Handles the page for the symptoms.
    """

    def get(self):
        """
        Serves the page for showing all symptoms in the database.
        """
        return render_template("symptoms.html",
                               symptoms=get_db().get_all_symptoms())


@app.route('/app_doctors')
def view_apps_by_doctors():
    """
    Serves a page which shows the database organized by doctor.
    """
    return render_template("app_by_doctors.html",
                           apps_by_doctor=get_app_by_doctor())


@app.route('/app_months')
def view_apps_months():
    """
    Serves a page which shows the database organized by scheduled month.
    """
    return render_template("app_by_months.html",
                           apps_by_month=get_app_by_month())


# Additional feature for the project
# Create a html page that enables the user to add a new appointment to
# the database.
# If the user hits the submit button to get to this page, it will be a POST
# request

@app.route('/add', methods=['GET', 'POST'])
def add():
    # These variables will be changed if an appointment was added,
    # so that we can display some extra text.
    display_notice = False
    successful_add = None
    notice_text = None

    # If all parameters for an appointment were submitted then those
    # parameters will be keys in the request.form dictionary.

    if ('first_name' in request.form and 'last_name' in request.form and
            'gender' in request.form and 'age' in request.form and 'doctor' in
            request.form and 'month' in request.form and 'symptom' in
            request.form and 'birth' in request.form):
        display_notice = True

        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        gender = request.form['gender'].strip()
        age = request.form['age'].strip()
        birth = request.form['birth'].strip()
        doctor = request.form['doctor'].strip()
        month = request.form['month'].strip()
        symptom = request.form['symptom'].strip()

        max_length = 20

        if (first_name == '' or last_name == '' or gender == ''
                or age == '' or doctor == '' or month == '' or symptom == ''
                or birth == ''):
            successful_add = False
            notice_text = 'You must enter all of the information!'
        elif (len(first_name) > max_length or len(last_name) > max_length or
              len(gender) > max_length or len(age) > max_length or
              len(doctor) > max_length or len(month) > max_length or
              len(symptom) > max_length or len(birth) > max_length):
            successful_add = False
            notice_text = 'All information must be at most 20 characters long!'
        else:
            successful_add = True
            notice_text = 'Appointment is successfully made!'
            get_db().insert_app(first_name, last_name, gender, age, birth,
                                doctor, month, symptom)

    return render_template('add.html', display_notice=display_notice,
                           add_status=successful_add,
                           notice_message=notice_text)


# Register MainView as the handler for the homepage of the website
main_view = MainView.as_view('main_view')
app.add_url_rule('/', view_func=main_view, methods=['GET'])

# Register AppsView as the handler for all the /apps requests
apps_view = AppsView.as_view('apps_view')
app.add_url_rule('/apps', view_func=apps_view, methods=['GET'])

# Register PatientsView as the handler for all the /patients requests
patients_view = PatientsView.as_view('patients_view')
app.add_url_rule('/patients', view_func=patients_view, methods=['GET'])

# Register DoctorsView as the handler for all the /books/ requests
doctors_view = DoctorsView.as_view('doctors_view')
app.add_url_rule('/doctors', view_func=doctors_view, methods=['GET'])

# Register SymptomsView as the handler for all the /symptoms requests
symptoms_view = SymptomsView.as_view('symptoms_view')
app.add_url_rule('/symptoms', view_func=symptoms_view, methods=['GET'])


if __name__ == "__main__":
    app.run(debug=True)
