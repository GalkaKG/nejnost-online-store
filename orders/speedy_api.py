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


def create_speedy_shipment(order, token):
    url = f"{settings.SPEEDY_BASE_URL}/shipment"

    payload = {
        "sender": {
            "partnerId": 123456789,  # ID-то на твоя фирмен акаунт
            "contactName": "Твоята фирма",
            "phone": "+359888888888",
            "email": "shop@example.com",
            "address": {
                "city": "София",
                "postalCode": "1000",
                "street": "ул. Примерна",
                "streetNo": "1"
            }
        },
        "recipient": {
            "contactName": order.user.get_full_name(),
            "phone": order.user.profile.phone,
            "email": order.user.email,
            "address": {
                "city": "Град",
                "postalCode": "1000",
                "street": order.address if order.delivery_type == "address" else "",
                "officeId": order.speedy_office_id if order.delivery_type == "office" else None
            }
        },
        "service": {
            "type": "DOOR_TO_DOOR" if order.delivery_type == "address" else "DOOR_TO_OFFICE",
            "parcelsCount": 1
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
