import os
import requests
from dotenv import load_dotenv
load_dotenv()

LEMONSQUEEZY_API_KEY = os.getenv('LEMONSQUEEZY_API_KEY')
LEMONSQUEEZY_STORE_ID = os.getenv('LEMONSQUEEZY_STORE_ID')
LEMONSQUEEZY_STANDARD_PRODUCT_ID = os.getenv('LEMONSQUEEZY_STANDARD_PRODUCT_ID')


def generate_razorpay_payment_link(name, email, image_link, gender):
    return None


def get_product_id_from_pack_type(pack_type):
    return LEMONSQUEEZY_STANDARD_PRODUCT_ID


def generate_lemonsqueezy_payment_link(name, email, user_id,pack_type):

    product_id = get_product_id_from_pack_type(pack_type)
    url = "https://api.lemonsqueezy.com/v1/checkouts"
    headers = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json',
        'Authorization': f'Bearer {LEMONSQUEEZY_API_KEY}'
    }
    payload = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "checkout_data": {
                    "name": name,
                    "email": email,
                    "custom": {
                        "user_name": name,
                        "email": email,
                        "user_id": user_id,
                        "pack_type": pack_type
                    }
                }
            },
            "relationships": {
                "store": {
                    "data": {
                        "type": "stores",
                        "id": LEMONSQUEEZY_STORE_ID
                    }
                },
                "variant": {
                    "data": {
                        "type": "variants",
                        "id": product_id
                    }
                }
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201 or response.status_code == 200:

        payment_link = response.json()["data"]["attributes"]["url"]
        return payment_link
    else:
        raise Exception(f"Error: {response.status_code}")