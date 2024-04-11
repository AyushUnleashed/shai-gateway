from database.handle_orders_db_updates import check_existing_order, insert_new_order
from database.supabase_utils import SUPABASE_CLIENT
from slack_bot.slackbot import SHAI_Slack_Bot
from process_payments_helper import get_current_payment_mode_from_order_id
async def validate_and_process_request_razorpay(order_data):
    try:
        exists, _ = check_existing_order(SUPABASE_CLIENT, order_data.order_id)
        if exists:
            return "Razorpay Order already exists. No action taken."

        await insert_new_order(order_data.__dict__)

        curr_mode = get_current_payment_mode_from_order_id(order_data.order_id)
        await SHAI_Slack_Bot.send_message(
            f"{curr_mode}: \n Razorpay Payment done:\n  user ID: {order_data.user_id} \n email: {order_data.email} \n order created with ID: {order_data.order_id}"
        )
    except Exception as e:
        return f"An error occurred while processing the Razorpay order: {str(e)}"
