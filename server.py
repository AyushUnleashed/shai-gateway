from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client

app = FastAPI()
from supabase_utils import SUPABASE_CLIENT


class WebhookPayload(BaseModel):
    data: dict
    meta: dict


@app.post("/webhook/")
async def receive_webhook(payload: WebhookPayload):
    """
    Endpoint to receive webhook payload.
    """
    # Check if the 'event' field is present in the 'meta' dictionary
    event_name = payload.meta.get('event_name', 'Unknown')

    custom_data = payload.meta.get('custom_data', {})
    first_order_item = payload.data['attributes']['first_order_item']

    print("Event Name:", event_name)
    print("Custom Data:")
    print(custom_data)

    print("\nFirst Order Item:")
    print("Variant ID:", first_order_item['variant_id'])
    print("Product Name:", first_order_item['product_name'])
    print("Created At:", first_order_item['created_at'])
    print("Price:", first_order_item['price'])
    print("Order id:", first_order_item['order_id'])
    print("Test mode:", first_order_item['test_mode'])

    # Insert data into the 'orders' table
    order_data = {
        "order_id": first_order_item['order_id'],
        "created_at": first_order_item['created_at'],
        "email": custom_data.get('email', ''),
        "user_name": custom_data.get('user_name', ''),
        "gender": custom_data.get('gender', ''),
        "user_image_link": custom_data.get('user_image_link', ''),
        "status": "NOT_PROCESSED",
        "product_name": first_order_item['product_name'],
        "webhook_object": payload.model_dump(),
        "test_mode": first_order_item['test_mode']
    }

    # Execute the query and unpack the tuple response


    response_tuple = SUPABASE_CLIENT.table('orders').select("*").eq('order_id', order_data['order_id']).execute()

    # The response is expected to be a tuple, let's unpack it
    response_data, response_metadata = response_tuple

    # Log the response for debugging
    print("Response data:", response_data)
    print("Response metadata:", response_metadata)

    # Check if the 'metadata' part indicates an actual error or just contains 'count' with None
    if response_metadata and response_metadata[0] == 'count' and response_metadata[1] is None:
        # This scenario is treated as a successful response without an actual error
        error = None
    else:
        # If response_metadata does not match the 'count' with None pattern, treat it as an error
        error = response_metadata

    if error:
        print(f"Unexpected error querying Supabase: {error}")
        raise HTTPException(status_code=400, detail="Unexpected error querying Supabase.")

    # Check if any records exist in the response_data
    if response_data and len(response_data[1]) > 0:
        # Data exists, meaning the order already exists
        print("Order already exists, not inserting.")
        return {"message": "Order already exists. No action taken."}
    else:
        # No existing data found, proceed to insert new order
        insert_response, insert_error = SUPABASE_CLIENT.table('orders').insert(order_data).execute()
        if insert_error and insert_error[0] == 'count' and insert_error[1] is not None:
            print(f"Error inserting into Supabase: {insert_error}")
            raise HTTPException(status_code=400, detail="Error inserting data into Supabase.")

    return {"message": "Webhook received and data processed successfully."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5151)
