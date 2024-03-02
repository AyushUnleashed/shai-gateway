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

if __name__ == "__main__":
    import asyncio
    order = asyncio.run(create_order(
        name="John Doe",
        email="ayushyadavcodes@gmail.com",
        user_id="123",
        pack_type="STANDARD"
    ))
    print("order", order)
    print("order_id", order["id"])
    print("notes", order["notes"])