from webhook_supabase_handler import check_existing_order, insert_new_order

# async def validate_and_process_request_razorpay()
#
#     exists, _ = check_existing_order(order_data['order_id'])
#     if exists:
#         return "Order already exists. No action taken."
#
#     await insert_new_order(order_data)