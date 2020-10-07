# Patients-Appointments-Management-System
Created and Written by Minhwa Lee

## Introduction
This file is a Flask implementation for healthcare providers to manage appointments that provides patient management API 
and related HTML pages.


## API Information
First, the API for this project provides information about the appointments that
have been scheduled or the records of the previous appointments. This would let 
the user to access and manage information about the appointments efficiently. In addition to 
the appointment schedules, this API provides the records of patients, doctors, or 
symptoms. 

### app_db.py
The file 'app_db' contains a class named 'AppointmentDataBase' to encapsulate access to 
the database named 'appointments.sqlite.' In the class there are many functions for each table 'doctors', 'patients', 
'symptoms', and 'appointments.' Those functions are later used in the APIs. 

### tests.py 

This file includes all pytest tests that demonstrate the correctness of codes 
used in the all functions of the class 'AppointmentDataBase.'

### app_api.py

This is a Flask application that provides an API for 
accessing and modifying the data in the database 'appointments.sqlite.'
You can get, post, and delete data about appointments, patients, doctors, and symptoms in each requests 
through terminal. 

### app_api_html.py

This is a HTML version of the Flask application that
provides a management API, which presents information from the
database as a web page using an HTML template. 

Running on the localhost, you can access appointments, patients, 
doctors, and symptoms, and also can add information about appointments directly to the database 
in a HTML form. 

### app_command_api.py

This is a command-line application that uses Python's requests module
to use a management API. This application presents information of 
appointments, patients, doctors, and symptoms in the database. 

### templates / static

The folder 'templates' contains all HTML files for web pages that 
have been used in the file app_api_html.py. 

The folder 'static' contains a CSS file to add some background color and 
to change font type used in the HTML pages. 



 
