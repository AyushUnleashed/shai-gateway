from httpx import AsyncClient
from fastapi import HTTPException

async def create_order(name: str, email: str, user_id: str, pack_type: str):
    async with AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:5151/payments/razorpay/create_order",
                json={
                    "name": name,
                    "email": email,
                    "user_id": user_id,
                    "pack_type": pack_type
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        

from pydantic import BaseModel

class DummyUpdatePaidUserDBRequest(BaseModel):
    order_id: str
    user_id: str
    gender: str

async def send_dummy_update_paid_user_db_request(order_id: str, user_id: str, gender: str):
    dummy_request = DummyUpdatePaidUserDBRequest(
        order_id=order_id,
        user_id=user_id,
        gender=gender
    )
    async with AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:5151/update_paid_user_db",
                json=dummy_request.dict()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import asyncio
    async def main():
        # order = await create_order(
        #     name="John Doe",
        #     email="ayushyadavcodes@gmail.com",
        #     user_id="123",
        #     pack_type="STANDARD"
        # )
        # print("order", order)
        # print("order_id", order["id"])
        # print("notes", order["notes"])
        
        # Send dummy update paid user db request
        update_response = await send_dummy_update_paid_user_db_request(
            order_id="order_NiOpQWe5qUSThf",
            user_id="user_2cr7AG6HKHUwRSsSUQvUy4bmP9v",
            gender="MALE"
        )
        print("update_response", update_response)

    asyncio.run(main())

    
