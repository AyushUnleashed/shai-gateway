import os
from dotenv import load_dotenv
from supabase import create_client, Client 
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

import login, sign_up

def main():

    user = sign_up.sign_up(supabase_client=supabase_client,
        users_email="ayushyadavytube@gmail.com",
        users_password="123456"
    )
    print(user)

if __name__ == "__main__":
    main()