from pydantic import BaseModel
from typing import Dict, Any

class WebhookPayload(BaseModel):
    data: Dict[str, Any]
    meta: Dict[str, Any]