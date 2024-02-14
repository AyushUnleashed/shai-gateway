import datetime
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')



def create_supabase_client():
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase_client

SUPABASE_CLIENT = create_supabase_client()