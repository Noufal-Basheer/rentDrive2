import requests
from cli_utils import constants
from cli_utils.logger import registry
from cli_utils.logger.logger import p

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
        print("Error: %s"%response.text)
        return False


def get_ticket_data():
    url = constants.FASTAPI_URL + "/purchase/id"
    auth_token = registry.get_registry("auth_token")
    if not auth_token:
        p.info("unable to update, login to continue")
        return False
    headers = {
    "Authorization": "Bearer " + auth_token ,
    "accept": "application/json",
}
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            p.info("ticket fetched successfully")
            if response.json():
                registry.set_registry("ticket_id", response.json().get("_id"))
                registry.set_registry("lender_id", response.json().get("lender_id"))
                registry.set_registry("lentee_id", response.json().get("lentee_id"))
            return response.json()
        else:
            p.info("Failed fetch ticket detials %s"%response.text)
            return False
    except Exception as e:
        p.info(f"update_ip_address : {e}")

def get_lender_ip():
    url = constants.FASTAPI_URL + "/purchase/ip_address"
    auth_token = registry.get_registry("auth_token")
    if not auth_token:
        p.info("unable to update, login to continue")
        return False
    headers = {
    "Authorization": "Bearer " + auth_token ,
    "accept": "application/json",
}
    lender_id = registry.get_registry("lender_id")
    if not lender_id:
        lender_id = "1234"
    param = {"id":lender_id}
    try:
        response = requests.get(url,headers=headers,params=param)
        if response.status_code == 200:
            p.info("ip fetched successfully")
            return response.json()
        else:
            p.info("Failed fetch ticket detials %s"%response.text)
            return False
    except Exception as e:
        p.info(f"update_ip_address : {e}")
        return False
