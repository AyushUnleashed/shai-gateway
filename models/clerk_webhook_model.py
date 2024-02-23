from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl

# === Verification Models ===
class LinkedTo(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None

class Verification(BaseModel):
    attempts: Optional[int] = None
    expire_at: Optional[int] = None
    status: Optional[str] = None
    strategy: Optional[str] = None

class EmailVerification(BaseModel):
    attempts: Optional[int] = None
    expire_at: Optional[int] = None
    status: Optional[str] = None
    strategy: Optional[str] = None

# === E-mail Address Model ===
class Email(BaseModel):
    email_address: Optional[EmailStr] = None
    id: Optional[str] = None
    linked_to: Optional[List[LinkedTo]] = None
    object: Optional[str] = None
    reserved: Optional[bool] = None
    verification: Optional[EmailVerification] = None

# === Accounts & Services Models ===
class ExternalAccount(BaseModel):
    approved_scopes: Optional[str] = None
    email_address: Optional[EmailStr] = None
    family_name: Optional[str] = None
    given_name: Optional[str] = None
    google_id: Optional[str] = None
    id: Optional[str] = None
    object: Optional[str] = None
    label: Optional[str] = None
    picture: Optional[HttpUrl] = None
    username: Optional[str] = None
    verification: Optional[Verification] = None
    public_metadata: Optional[dict] = None

# === Main User Webhook Data Event Payload Model ===
class BodyModel(BaseModel):
    backup_code_enabled: Optional[bool] = None
    banned: Optional[bool] = None
    create_organization_enabled: Optional[bool] = None
    created_at: Optional[int] = None
    delete_self_enabled: Optional[bool] = None
    email_addresses: Optional[List[Email]] = None
    external_accounts: Optional[List[ExternalAccount]] = None
    first_name: Optional[str] = None
    has_image: Optional[bool] = None
    id: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    last_active_at: Optional[int] = None
    last_name: Optional[str] = None
    last_sign_in_at: Optional[int] = None
    locked: Optional[bool] = None
    object: Optional[str] = None
    phone_numbers: Optional[List] = None
    primary_email_address_id: Optional[str] = None
    totp_enabled: Optional[bool] = None
    two_factor_enabled: Optional[bool] = None
    updated_at: Optional[int] = None
    private_metadata: Optional[dict] = None
    profile_image_url: Optional[HttpUrl] = None
    public_metadata: Optional[dict] = None

class ClerkWebhookPayload(BaseModel):
    data: BodyModel
    object: str
    type: str
