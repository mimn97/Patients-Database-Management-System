"""
This is a command-line application that uses Python's requests module to use a
management API. This application presents information of appointments, patients,
doctors, and symptoms in the database. It interacts with the website through
the API.

Written by Minhwa (Mina) Lee
"""

import requests
import sys

API_BASE_URL = 'http://127.0.0.1:5000/'


def main():
    """
    Fetch a response object with information from the database by using
    primary key of the object.

    :return a response object with the primary key
    """

    web_page = input("Enter the name of pages you want to access "
                     "(apps, patients, doctors, or symptoms): ").strip()

    if web_page not in ['apps', 'patients', 'doctors', 'symptoms']:
        print("You must enter the correct name of the web pages.")
        sys.exit()

    ans = input("Do you want to fetch an information with specific key? "
                "(Yes/No) ")

    if ans == 'Yes':
        key = input("Enter the primary key that you want to see: ")
        request_url = '{}/{}/{}'.format(API_BASE_URL, web_page, key)
        response = requests.get(request_url)
    elif ans == 'No':
        request_url = '{}/{}'.format(API_BASE_URL, web_page)
        response = requests.get(request_url)

    content = response.json()

    print("\nHere is the information.")

    # If presents all information in the list (post)
    if isinstance(content, list):
        for result in content:
            for key in result:
                print("{} : {}".format(key, result[key]))
            print('\n')

    else:  # If it's in dictionary form
        for key in content:
            print("{} : {}".format(key, content[key]))
        print('\n')


if __name__ == '__main__':
    main()
