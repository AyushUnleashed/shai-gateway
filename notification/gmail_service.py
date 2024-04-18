import smtplib
from email.mime.text import MIMEText
from utils.config import settings
from utils import constants

def send_email(subject, body, sender, recipients, server='smtp.gmail.com', port=465):
    password = settings.GOOGLE_APP_PASSWORD
    """
    Send an email using SMTP with SSL.

    Parameters:
    - subject (str): The subject line of the email.
    - body (str): The body text of the email.
    - sender (str): The sender's email address.
    - recipients (list): A list of email addresses to send the email to.
    - password (str): The password for the sender's email account.
    - server (str): The SMTP server to connect to.
    - port (int): The port number to use for the SMTP server connection.

    Returns:
    - None
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    try:
        with smtplib.SMTP_SSL(server, port) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Email sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_image_via_gmail(user_email,image_url):
    recipients = [user_email]
    subject = "Your Superhero Image is Ready!"
    body = f"""
       Hello,

       Your superhero image has been generated and is now available in your account's gallery.

       You can view your image here: {image_url}

       Best regards,
       Ayush - Founder,
       SuperHeroAI 
       """
    send_email(subject, body, constants.SENDER_EMAIL, recipients)



if __name__ == "__main__":
    # subject = "Email Subject"
    # body = "This is the body of the text message."
    # sender = "ayushyadavcodes@gmail.com"
    # recipients = ["ayushyadavytube@gmail.com"]
    #
    # send_email(subject, body, sender, recipients)
    image_url = "https://mvlmexldvleywcfmvzwt.supabase.co/storage/v1/object/public/free-user-images/user_user_2dn0xb5utBAiH2r7f4Pm7929L7f/image_4c5d869a-2563-449c-9282-bc8d56711e75.png?"
    send_image_via_gmail("ayushyadavytube@gmail.com",image_url)
