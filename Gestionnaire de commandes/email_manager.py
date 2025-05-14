# email_manager.py
import smtplib
from config_loader import CONFIG

def send_email():
    sender_email = CONFIG["email"]["sender_email"]
    recipient_email = CONFIG["email"]["recipient_email"]
    app_password = CONFIG["email"]["app_password"]

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.login(user=sender_email, password=app_password)
        connection.sendmail(from_addr=sender_email,
                            to_addrs=recipient_email,
                            msg='Subject: Depassement du nombre de commandes permises\n\n Ce message est pour vous informer que vous avez plus de 10 commandes.')
