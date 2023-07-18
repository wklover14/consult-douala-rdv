import schedule
import time
import smtplib, ssl
import smtplib
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from scrapper import get_available_days

# Email details
sender_email = input("Entrer l'adresse email emetteur : ")
sender_password = getpass.getpass("Votre mot de passe : " )
recipient_email = input("Entrer l'adresse email du destinataire : ")
subject = "Availability Alert"

#server details 
smtp_server = input("Entrer l'adresse du serveur smtp de votre email : ")
server = smtplib.SMTP_SSL(smtp_server, 465)
server.login(sender_email, sender_password)

def check_availability():
	availability_found = get_available_days()
	if availability_found : send_email(availability_found)

def send_email(content = []):
    message = "There is availability on a specific day !" + ' || '.join(content)
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server.send_message(msg)

# Schedule the function to run every 2 hours
schedule.every(45).minutes.do(check_availability)

if __name__ == '__main__':
    print("\033[32m ****** SCRAPPER ***** \033[0m")
    check_availability()
    while True:
        schedule.run_pending()
        time.sleep(1)
