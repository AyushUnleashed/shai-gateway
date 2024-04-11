from database.supabase_utils import SUPABASE_CLIENT
from fastapi import HTTPException

def get_razor_pay_prices_from_db(pack_type):
    response = SUPABASE_CLIENT.table('pricing').select('amount').eq('payment_platform', 'RAZOR_PAY').eq('pack_type',
                                                                                                        pack_type).execute()
    response_data, response_error = response
    # Check for response error based on the count of error messages
    if response_error and response_error[0] == 'count' and response_error[1] is None:
        # No error
        error = None
    else:
        # Error exists
        error = response_error

    if error:
        raise HTTPException(status_code=400, detail=f"Unexpected error querying Supabase: {error}")

    amount = response_data[1][0].get("amount")
    return amount


def get_razor_pay_pack_data(pack_type):
    pack_type = pack_type.upper()

    razor_pay_inr_pack_prices = [
        'BASIC',
        'STANDARD',
        'PRO'
    ]
    if pack_type not in razor_pay_inr_pack_prices:
        raise ValueError(f"Invalid pack type: {pack_type}. Valid pack types are: {list(razor_pay_inr_pack_prices)}")
    amount_in_inr = get_razor_pay_prices_from_db(pack_type)
    amount_in_paise = amount_in_inr * 100
    return str(amount_in_paise)


def create_razor_pay_order(name, email, user_id, pack_type):
    try:
        pack_amount_in_paise = get_razor_pay_pack_data(pack_type)
        import razorpay
        RAZOR_PAY_ID = os.getenv('RAZOR_PAY_ID')
        RAZOR_PAY_SECRET = os.getenv('RAZOR_PAY_SECRET')
        client = razorpay.Client(auth=(RAZOR_PAY_ID, RAZOR_PAY_SECRET))
        print("receipt:", "order_rcptid_{user_id}")
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

from utils.config import settings

# if __name__ == "__main__":
#     order = create_razor_pay_order(
#         name="John Doe",
#         email="ayushyadavcodes@gmail.com",
#         user_id="123",
#         pack_type="STANDARD"
#     )
#     print("order", order)
#     print("order_id", order["id"])
#     print("notes", order["notes"])
#
if __name__ =="__main__":
    price= get_razor_pay_prices_from_db('PRO')
    print(price)