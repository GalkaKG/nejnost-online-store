import requests
from django.conf import settings


def get_speedy_token():
    url = f"{settings.SPEEDY_BASE_URL}/login"
    payload = {
        "username": settings.SPEEDY_USERNAME,
        "password": settings.SPEEDY_PASSWORD
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["token"]


