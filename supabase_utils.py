import datetime
from config import settings
from supabase import create_client, Client



def create_supabase_client():
    supabase_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return supabase_client

SUPABASE_CLIENT = create_supabase_client()