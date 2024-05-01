import requests
from cli_utils import constants

def login(name,password):
    payload={
        "username": name,
        "password": password
    }
    url = constants.FASTAPI_URL+"/login"
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Error:", response.text)
        return False


