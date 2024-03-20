import os
import requests
from dotenv import load_dotenv
load_dotenv()
from supabase_utils import SUPABASE_CLIENT, Client
from fastapi import  HTTPException
from logger import get_logger
logger = get_logger(__name__)

LEMONSQUEEZY_STORE_ID = os.getenv('LEMONSQUEEZY_STORE_ID')
LEMONSQUEEZY_STANDARD_PRODUCT_ID = os.getenv('LEMONSQUEEZY_STANDARD_PRODUCT_ID')

from configuration import CONFIG

def get_razor_pay_pack_data(pack_type):
    pack_type = pack_type.upper()

    BASIC_PACK_PRICE_INR = 1
    STANDARD_PACK_PRICE_INR = 830
    PRO_PACK_PRICE_INR = 1245

    razor_pay_inr_pack_prices = {
        'BASIC': BASIC_PACK_PRICE_INR,
        'STANDARD': STANDARD_PACK_PRICE_INR,
        'PRO': PRO_PACK_PRICE_INR
    }
    if pack_type not in razor_pay_inr_pack_prices:
        raise ValueError(f"Invalid pack type: {pack_type}. Valid pack types are: {list(razor_pay_inr_pack_prices.keys())}")
    amount_in_inr = razor_pay_inr_pack_prices[pack_type]
    amount_in_paise = amount_in_inr * 100
    return str(amount_in_paise)

def create_razor_pay_order(name, email, user_id, pack_type):
    try:
        pack_amount_in_paise = get_razor_pay_pack_data(pack_type)
        import razorpay
        RAZOR_PAY_ID = os.getenv('RAZOR_PAY_ID')
        RAZOR_PAY_SECRET = os.getenv('RAZOR_PAY_SECRET')
        client = razorpay.Client(auth=(RAZOR_PAY_ID, RAZOR_PAY_SECRET))
        print("receipt:","order_rcptid_{user_id}")
        data = {
            "amount": pack_amount_in_paise,
            "currency": "INR",
            "notes": {
                "user_name": name,
                "email": email,
                "user_id": user_id,
                "pack_type": pack_type
            }
        }
        order = client.order.create(data)
        return order
    
    except razorpay.errors.BadRequestError as err:
        print(f"Bad Request Error: {err}")
        raise
    except razorpay.errors.GatewayError as err:
        print(f"Gateway Error: {err}")
        raise
    except razorpay.errors.ServerError as err:
        print(f"Server Error: {err}")
        raise
    except Exception as err:
        print(f"An unexpected error occurred while creating razorpay order: {err}")
        raise

def get_product_id_from_pack_type(pack_type):
    from config import settings
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
        redirect_url = CONFIG.lemonsqueezy_frontend_redirect_url
        product_id, lemonsqueezy_api_key = get_product_id_from_pack_type(pack_type)
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

if __name__ == "__main__":
    order = create_razor_pay_order(
        name="John Doe",
        email="ayushyadavcodes@gmail.com",
        user_id="123",
        pack_type="STANDARD"
    )
    print("order", order)
    print("order_id", order["id"])
    print("notes", order["notes"])



def get_current_payment_mode(order_id: str):
    try:
        response_tuple = SUPABASE_CLIENT.table('orders').select("test_mode").eq('order_id', order_id).execute()
        print("response_tuple:", response_tuple)

        response_data, response_error = response_tuple

        # Check for response error based on the count of error messages
        if response_error and response_error[0] == 'count' and response_error[1] is None:
            # No error
            error = None
        else:
            # Error exists
            error = response_error

        if error:
            raise HTTPException(status_code=400, detail=f"Unexpected error querying Supabase: {error}")

        print("response_data:", response_data)
        test_mode = response_data[1][0].get("test_mode")
        curr_mode = "TEST" if test_mode else "PROD"

    except Exception as e:
        logger.error(f"Error determining payment platform mode: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while determining payment mode.")
    return curr_mode
