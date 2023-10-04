import requests
from django.conf import settings

def get_pathao_access_token():
    base_url = settings.PATHAO_API_BASE_URL
    client_id = settings.PATHAO_CLIENT_ID
    client_secret = settings.PATHAO_CLIENT_SECRET
    client_email = settings.PATHAO_CLIENT_EMAIL
    client_password = settings.PATHAO_CLIENT_PASSWORD
    grant_type = settings.PATHAO_GRANT_TYPE

    auth_url = f"{base_url}/oauth/token"

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "username": client_email,
        "password": client_password,
        "grant_type": grant_type,
    }

    response = requests.post(auth_url, data=data)
    print(response, '-------------------------------------')

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to obtain Pathao access token")


# pathao_integration/services.py

def create_pathao_shipment(shipment_data, access_token):
    base_url = settings.PATHAO_API_BASE_URL
    shipment_url = f"{base_url}/api/shipments/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(shipment_url, headers=headers, json=shipment_data)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception("Failed to create Pathao shipment")



# def create_pathao_shipment(shipment_data, access_token):
#     base_url = settings.PATHAO_API_BASE_URL
#     shipment_url = f"{base_url}/api/shipments/"

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json",
#     }

#     response = requests.post(shipment_url, headers=headers, json=shipment_data)

#     if response.status_code == 201:
#         return response.json()
#     else:
#         raise Exception("Failed to create Pathao shipment")
    
