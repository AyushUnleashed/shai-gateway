from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import json


class Status(Enum):
    NOT_GENERATED = "NOT_GENERATED"
    GENERATING = "GENERATING"
    GENERATED = "GENERATED"
    SENT = "SENT"


class PaymentPlatform(Enum):
    LEMON_SQUEEZY = "LEMON_SQUEEZY"
    RAZOR_PAY = "RAZOR_PAY"


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


@dataclass
class OrderData:
    order_id: str
    created_at: str
    email: str
    payment_platform: PaymentPlatform  # Assuming it's a required field without a default
    user_id: str
    gender: Optional[Gender]  # Default to NOT_SPECIFIED or None if you prefer
    user_name: Optional[str] = ""  # Made optional with a default empty string
    user_image_link: Optional[str] = ""
    status: Status = Status.NOT_GENERATED
    pack_type: Optional[str] = ""
    webhook_object: str = field(default_factory=lambda: "{}")
    custom_data: Optional[str] = None
    test_mode: bool = True


    def __post_init__(self):
        # Convert webhook_object string back to a dictionary if needed elsewhere in your code
        self.webhook_object = json.loads(self.webhook_object)
