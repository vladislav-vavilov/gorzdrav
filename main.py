import requests
from config import BASE_URL


def get_districts():
    try:
        response = requests.get(f'{BASE_URL}/_api/api/v2/shared/districts')

        if response.status_code == 200:
            return response.json()

        raise Exception('Could not get districts')
    except Exception as error:
        print(error)


get_districts()
