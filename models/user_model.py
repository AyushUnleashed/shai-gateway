from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional, Union

class User(BaseModel):
    user_id: str
    email: Optional[EmailStr]
    credits: Optional[int]
    orders_array: Optional[List[str]]
    user_image_link: Optional[HttpUrl]
    gender: Optional[str]
    test_mode:bool