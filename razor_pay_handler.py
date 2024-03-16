from webhook_supabase_handler import check_existing_order, insert_new_order
from supabase_utils import SUPABASE_CLIENT, Client
from slackbot import SHAI_Slack_Bot

async def validate_and_process_request_razorpay(order_data):
    try:
        exists, _ = check_existing_order(SUPABASE_CLIENT, order_data.order_id)
        if exists:
            return "Razorpay Order already exists. No action taken."

        await insert_new_order(order_data.__dict__)
        await SHAI_Slack_Bot.send_message(
            f"Razorpay Payment done:\n  user ID: {order_data.user_id} \n email: {order_data.email} \n order created with ID: {order_data.order_id}"
        )
    except Exception as e:
        return f"An error occurred while processing the Razorpay order: {str(e)}"
