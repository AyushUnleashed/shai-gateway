# logic to sign in the app


def sign_up(supabase_client, users_email, users_password):

    try:
        user = supabase_client.auth.sign_up({
            "email": users_email,
            "password": users_password 
            })
        
        # add 1 free credit to the user
        return user
    except(Exception):
        print("Error occured:", Exception)
        return None
