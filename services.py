import requests
from config import BASE_URL
from datetime import datetime


def get_districts():
    try:
        response = requests.get(f'{BASE_URL}/shared/districts')

        if response.status_code == 200:
            return response.json()

        raise Exception('Could not get districts')
    except Exception as error:
        print(error)


def get_clinics(district_id):
    try:
        response = requests.get(
            f'{BASE_URL}/shared/district/{district_id}/lpus')

        if response.status_code == 200:
            return response.json()

        raise Exception('Could not get clinics')
    except Exception as error:
        print(error)


def get_specialties(clinic_id):
    try:
        response = requests.get(
            f'{BASE_URL}/schedule/lpu/{clinic_id}/specialties')

        if response.status_code == 200:
            return response.json()

        raise Exception('Could not get specialties')
    except Exception as error:
        print(error)


def get_doctors(clinic_id, specialty_id):
    try:
        response = requests.get(
            f'{BASE_URL}/schedule/lpu/{clinic_id}/speciality/{specialty_id}/doctors')

        if response.status_code == 200:
            return response.json()

        raise Exception('Could not get doctors')
    except Exception as error:
        print(error)


def get_appointments(clinic_id, doctor_id):
    try:
        response = requests.get(
            f'{BASE_URL}/schedule/lpu/{clinic_id}/doctor/{doctor_id}/appointments')

        if response.status_code == 200:
            return response.json()

        raise Exception('Could not get appointments')
    except Exception as error:
        print(error)


def check_patient(clinic_id, last_name, first_name, middle_name, birthdate):
    try:
        data = {
            'lpuId': clinic_id,
            'lastName': last_name,
            'firstName': first_name,
            'middleName': middle_name,
            'birthdate': datetime.strptime(birthdate, '%d.%m.%Y').isoformat(),
            'birthdateValue': birthdate,
        }

        response = requests.get(f'{BASE_URL}/patient/search', data=data)

        if response.status_code == 200:
            return response.json()

        raise Exception('Could not check patient')
    except Exception as error:
        print(error)


def create_appointment(clinic_id, appointment, patient):
    checking_data = check_patient(
        clinic_id=clinic_id,
        last_name=patient['last_name'],
        first_name=patient['first_name'],
        middle_name=patient['middle_name'],
        birthdate=patient['birthdate'],
    )

    if checking_data is None or 'result' not in checking_data:
        raise Exception('No patient was found')

    data = {
        'esiaId': None,
        'lpuId': clinic_id,
        'patientId':  checking_data['result'],
        'appointmentId': appointment['id'],
        'referralId': None,
        'ipmpiCardId': None,
        'recipientEmail': patient['email'],
        'patientLastName': patient['last_name'],
        'patientFirstName': patient['first_name'],
        'patientMiddleName': patient['middle_name'],
        'patientBirthdate': patient['birthdate'],
        'room': appointment['room'],
        'num': appointment['number'],
        'address': appointment['address'],
        'visitDate': appointment['visitStart'],
    }

    response = requests.get(f'{BASE_URL}/appointment/create', data=data)
    print(response)


def search_appointments():
    '''
        /appointments
        data: {
                lpuId: lpuId,
                patientId: patientId
            },


        /appointments/search
        data: {
                sessionId,
                profileId
            },
    '''
