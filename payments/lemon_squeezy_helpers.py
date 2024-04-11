import os
import requests
from dotenv import load_dotenv
load_dotenv()
from utils.logger import get_logger
logger = get_logger(__name__)
from utils.config import settings

LEMONSQUEEZY_STORE_ID = os.getenv('LEMONSQUEEZY_STORE_ID')
LEMONSQUEEZY_STANDARD_PRODUCT_ID = os.getenv('LEMONSQUEEZY_STANDARD_PRODUCT_ID')


def get_product_id_from_pack_type_lmnsqzy(pack_type):
    from utils.config import settings
    pack_type = pack_type.upper()
    product_id = ''
    if settings.IS_TEST_MODE:
        lemonsqueezy_api_key = settings.LEMONSQUEEZY_API_TEST_KEY
        if pack_type == 'BASIC':
            product_id = settings.LEMONSQUEEZY_BASIC_TEST_PRODUCT_ID
        elif pack_type == 'STANDARD':
            product_id = settings.LEMONSQUEEZY_STANDARD_TEST_PRODUCT_ID
        elif pack_type == 'PRO':
            product_id = settings.LEMONSQUEEZY_PRO_TEST_PRODUCT_ID
    else:
        lemonsqueezy_api_key = settings.LEMONSQUEEZY_API_KEY
        if pack_type == 'BASIC':
            product_id = settings.LEMONSQUEEZY_BASIC_PRODUCT_ID
        elif pack_type == 'STANDARD':
            product_id = settings.LEMONSQUEEZY_STANDARD_PRODUCT_ID
        elif pack_type == 'PRO':
            product_id = settings.LEMONSQUEEZY_PRO_PRODUCT_ID

    return product_id,lemonsqueezy_api_key
    raise ValueError(f"Invalid pack type: {pack_type}")

def generate_lemonsqueezy_payment_link(name, email, user_id, pack_type):
    try:
        redirect_url = settings.lemonsqueezy_frontend_redirect_url
        product_id, lemonsqueezy_api_key = get_product_id_from_pack_type_lmnsqzy(pack_type)
        url = "https://api.lemonsqueezy.com/v1/checkouts"
        headers = {
            'Accept': 'application/vnd.api+json',
            'Content-Type': 'application/vnd.api+json',
            'Authorization': f'Bearer {lemonsqueezy_api_key}'
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
                    },
                    "product_options": {
                        "redirect_url": redirect_url
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
        response.raise_for_status()  # Raises HTTPError for bad requests (4XX or 5XX)

        payment_link = response.json()["data"]["attributes"]["url"]
        return payment_link

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        raise
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        raise
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred while handling the request: {req_err}")
        raise
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
        raise