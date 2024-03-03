from webhook_supabase_handler import check_existing_order, insert_new_order
from supabase_utils import SUPABASE_CLIENT, Client


async def validate_and_process_request_razorpay(order_data):
    exists, _ = check_existing_order(SUPABASE_CLIENT, order_data.order_id)
    if exists:
        return "Razorpay Order already exists. No action taken."

    await insert_new_order(order_data.__dict__)
