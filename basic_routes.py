from fastapi import FastAPI, HTTPException, Request
from routers import basic_router
from pydantic import BaseModel
from supabase_utils import SUPABASE_CLIENT
supabase = SUPABASE_CLIENT

# class UpdatePaidUserDBRequest(BaseModel):
#     order_id: str
#     user_id: str
#     gender: str
#
# @basic_router.post("/update_paid_user_db")
# async def update_paid_user_db(request: UpdatePaidUserDBRequest):
#     # Get image link from Supabase Storage
#     image_path = f"{request.user_id}/{request.order_id}.png"
#     image_link_response = supabase.storage.from_('paid-user-images').get_public_url(image_path)
#     image_link = image_link_response.data.get('publicURL')
#
#     if not image_link:
#         raise HTTPException(status_code=404, detail="Image link not found")
#
#     # Update orders table with image link and gender
#     orders_table = supabase.table('orders')
#     update_response = orders_table.update({
#         'user_image_link': image_link,
#         'gender': request.gender,
#         'status': 'GENERATING'
#     }).eq('order_id', request.order_id).execute()
#
#     if update_response.error:
#         raise HTTPException(status_code=400, detail=f"Failed to update order: {update_response.error}")
#
#     return {"message": "Order updated successfully", "image_link": image_link}
