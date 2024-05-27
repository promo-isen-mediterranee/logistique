import pika
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

import urllib3
from controller import *
from dotenv import load_dotenv

load_dotenv()
api_user = os.getenv('API_USER')

channel = None


# reserve_item(event, type: str = "", label: str = "", nbr: int = 0)
# get_overlapping_events(event)
# find_item(name: str = "", type:str = "")
# update_stock(event, label, type, nbr)
# minimal_stock(event, type, label)


# A MODIFIER UNE FOIS QUE ROLE EST IMPLEMENTE -------------------------------------
def send_email(subject, alert, sender, receiver, role="Responsable"):
    msg = MIMEMultipart('alternative')

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    
    html1 = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Notification IMS Promo</title>
    """

    css1 = """
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        .header { background: #f0f0f0; padding: 10px; text-align: center; }
        .content { margin: 20px; }
        .footer { background: #f0f0f0; padding: 10px; text-align: center; }
        img { max-width: 100%; }
        .btn {
            background-color: #005AA7; /* Bleu ISEN */
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
            border: none;
        }
        .btn:hover {
            background-color: #FFD700; /* Jaune ISEN */
            color: #005AA7;
        }
    </style>
    """

    html2 = f"""
    </head>
    <body>
        <div class="header">
            <h1>IMS Promo Alert System</h1>
        </div>
        <div class="content">
            <h2>Alerte importante : {alert}</h2>
            <p>Cher/Chère {role},</p>
            <p>Une alerte importante a été détectée dans notre application. Veuillez vérifier immédiatement pour prendre les mesures nécessaires.</p>
            <p>Voici un aperçu de l'alerte :</p>
            <p>{alert}</p>
            <p><a href="https://promo.prinv.isen.fr/home" class="btn">Accéder à l'application</a></p>
        </div>
        <div class="footer">
            <p>Merci de votre attention,</p>
            <p>L'équipe IMS Promo</p>
        </div>
    </body>
    </html>
    """

    html_part = MIMEText(html1 + css1 + html2, 'html')

    msg.attach(html_part)
    
    server_name = "smtp.office365.com"
    server_port = 587
    # Connect to the SMTP server
    s = smtplib.SMTP(server_name, server_port, local_hostname='localhost')
    s.starttls()

    # ---------------------------
    # Login to the SMTP server
    password = "Rpwnwqy#4250216!"
    s.login(sender, password)
    s.set_debuglevel(1)
    # ---------------------------

    # Send the email
    s.send_message(msg)
    print("Email sent successfully")
    s.quit()

def get_mail_from_role(searchRole: str):
    allRole = urllib_to_json(urllib3.request.urlopen(f"{api_user}/auth/getAll"))
    searchMail = []
    for role in allRole:
        if role["role"] == searchRole:
            searchMail.append(role["email"])
    if searchMail == []:
        return None
    return searchMail

def send_email_to_role(subject, alert, sender, role):
    receiver = get_mail_from_role(role)
    if receiver == None:
        return f'Rôle fourni non trouvé, {role}', 404
    for mail in receiver:
        send_email(subject, alert, sender, mail, role)
    return f'Email envoyé à {role}', 200


def urllib_to_json(byte_obj):
    events = byte_obj.read()
    encoding = byte_obj.info().get_content_charset('utf-8')
    JSON_object = json.loads(events.decode(encoding))
    return JSON_object

def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    print("Connected to RabbitMQ")
    connection.channel(on_open_callback=on_channel_open)

def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.queue_declare(queue="test", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)
    print("Connected to the channel")

def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
    channel.basic_consume('test', handle_delivery)

def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    print(body)

def on_close(connection, exception):
    connection.ioloop.stop()
    print("Closing connection")


if __name__ == "__main__":

    credential = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(host="localhost", port=5672, credentials=credential)
    connection = pika.SelectConnection(on_open_callback=on_connected, on_close_callback=on_close)

    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start()

# Look at https://github.com/pika/pika/blob/main/examples/asynchronous_publisher_example.py
# for publishing example