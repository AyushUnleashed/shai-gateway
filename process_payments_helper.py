import os
import requests
from dotenv import load_dotenv
load_dotenv()

LEMONSQUEEZY_API_KEY = os.getenv('LEMONSQUEEZY_API_KEY')
LEMONSQUEEZY_STORE_ID = os.getenv('LEMONSQUEEZY_STORE_ID')
LEMONSQUEEZY_STANDARD_PRODUCT_ID = os.getenv('LEMONSQUEEZY_STANDARD_PRODUCT_ID')
RAZOR_PAY_API_KEY=os.getenv('RAZOR_PAY_API_KEY')

from configuration import CONFIG

def get_razor_pay_pack_data(pack_type):
    pack_type = pack_type.upper()

    BASIC_PACK_PRICE_INR = 820
    STANDARD_PACK_PRICE_INR = 1640
    PRO_PACK_PRICE_INR = 2460

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
    if settings.IS_TEST_MODE:
        if pack_type == 'BASIC':
            return settings.LEMONSQUEEZY_BASIC_TEST_PRODUCT_ID
        elif pack_type == 'STANDARD':
            return settings.LEMONSQUEEZY_STANDARD_TEST_PRODUCT_ID
        elif pack_type == 'PRO':
            return settings.LEMONSQUEEZY_PRO_TEST_PRODUCT_ID
    else:
        if pack_type == 'BASIC':
            return settings.LEMONSQUEEZY_BASIC_PRODUCT_ID
        elif pack_type == 'STANDARD':
            return settings.LEMONSQUEEZY_STANDARD_PRODUCT_ID
        elif pack_type == 'PRO':
            return settings.LEMONSQUEEZY_PRO_PRODUCT_ID
    raise ValueError(f"Invalid pack type: {pack_type}")

def generate_lemonsqueezy_payment_link(name, email, user_id,pack_type):

    redirect_url = CONFIG.lemonsqueezy_frontend_redirect_url
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
    if response.status_code == 201 or response.status_code == 200:

        payment_link = response.json()["data"]["attributes"]["url"]
        return payment_link
    else:
        raise Exception(f"Error: {response.status_code}")
    


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