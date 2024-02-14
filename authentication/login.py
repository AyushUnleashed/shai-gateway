# logic to login into the app

def login_user(supabase_client,users_email, users_password):
    user = supabase_client.auth.sign_in_with_password(email=users_email, password=users_password)
    return user