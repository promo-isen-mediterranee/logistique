import pika
import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import timedelta

from controller import *

api_user = os.getenv('API_USER')
api_stock = os.getenv('API_STOCK')
api_event = os.getenv('API_EVENT')

channel = None

def send_request(url):
    headers = {'X-BYPASS': os.getenv("BYPASS_TOKEN")}
    req = Request(url, headers=headers)
    return urllib_to_json(urlopen(req))

def update_current_stock():
    reserve_items = []
    items = urllib_to_json(urllib.request.urlopen(f"{api_stock}/item/getAll"))
    filtered_events = scan_events()
    for event in filtered_events:
        reserve_items = scan_reserved_items(event) 
        for item in items:
            for reserve_item in reserve_items:        
                if (item["item_id"]["id"] == reserve_item["item_location_id"]["item_id"]["id"]) and (reserve_item["status"] == False):
                    item["quantity"] -= reserve_item["quantity"]
                    update_stock = {
                        "name": item["item_id"]["name"],
                        "quantity": item["quantity"],
                        "location.id": item["location_id"]["id"],
                        "category": item["item_id"]["category_id"]["id"],
                    }
                    update_status  = {
                        "eventId": event["id"],
                        "item_locationId": reserve_item["item_location_id"]["id"],
                        "quantity": reserve_item["quantity"],
                        "status": True
                    }
                    data_stat = urllib.parse.urlencode(update_status).encode()
                    req_stat =  urllib.request.Request(f"{api_stock}/reservedItem/edit/{event['id']}/{item['id']}", data=data_stat, method="PUT")
                    resp_stat = urllib.request.urlopen(req_stat)   
                    data = urllib.parse.urlencode(update_stock).encode()
                    req =  urllib.request.Request(f"{api_stock}/item/{item['item_id']['id']}/{item['location_id']['id']}", data=data, method="PUT")
                    resp = urllib.request.urlopen(req)    
    return reserve_items
    

def scan_reserved_items(event):
    reserve_items = urllib_to_json(urllib.request.urlopen(f"{api_stock}/reservedItem/getAll"))
    filtered_reserved_items = [reserve_item 
                               for reserve_item in reserve_items 
                                if reserve_item["event_id"]["id"] == event["id"]]
    return filtered_reserved_items

def scan_events():
    # problème au niveau des dates : les heures ne seront pas prises en compte 
    # suite au getAll on a accès qu'aux jours et pas aux heures/minutes
    events = urllib_to_json(urllib.request.urlopen(f"{api_event}/getAll"))
    current_date = datetime.now()
    filtered_events = [
        event for event in events 
            if ( 
            datetime.strptime(event['date_start'], '%a, %d %b %Y %H:%M:%S %Z') - timedelta(days=2) <= current_date and
            datetime.strptime(event['date_end'], '%a, %d %b %Y %H:%M:%S %Z') + timedelta(days=1) >= current_date)
    ]
    return filtered_events
        

# A MODIFIER UNE FOIS QUE ROLE EST IMPLEMENTE -------------------------------------
def send_email_to_role(subject, alert, role = "ROLE_RESPONSABLE"):
    receiver = get_mail_from_role(role)
    print(receiver)
    # if receiver == None:
    #     return f'Rôle fourni non trouvé, {role}', 404
    # for mail in receiver:
    #     send_email(subject, alert, mail, role)
    # return f'Email envoyé à {role}', 200

from urllib.request import Request, urlopen

def get_mail_from_role(searchRole: str):
    url = f"{api_user}/auth/getRoles"
    headers = {'X-BYPASS': os.getenv("BYPASS_TOKEN")}
    req = Request(url, headers=headers)
    allRole = urllib_to_json(urlopen(req))

    searchMail = []
    print(allRole)
    # for role in allRole:
    #     if role["role"] == searchRole:
    #         searchMail.append(role["id_role"]["id_user"]["mail"])
    # if searchMail == []:
    #     return None
    # return searchMail

def send_email(subject, alert, receiver, role="Responsable"):
    msg = MIMEMultipart('alternative')

    sender = "alex.olivier.2502@gmail.com" # A modifier pour y intégrer le mail de l'ISEN
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


def urllib_to_json(byte_obj):
    print(byte_obj.read())
    # events = byte_obj.read()
    # encoding = byte_obj.info().get_content_charset('utf-8')
    # JSON_object = json.loads(events.decode(encoding))
    # return JSON_object

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