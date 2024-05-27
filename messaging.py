import pika
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

channel = None

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
            <p>Pour plus de détails, accédez à l'application IMS Promo.</p>
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

    # Login to the SMTP server
    password = "Rpwnwqy#4250216!"
    s.login(sender, password)
    s.set_debuglevel(1)

    # Send the email
    s.send_message(msg)
    print("Email sent successfully")
    s.quit()
    
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