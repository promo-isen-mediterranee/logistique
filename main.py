from customTypes import _event
from controller import urllib_to_json, update_stock
import urllib.request
import json
from controller import reserve_items

def checkMsg(body: str):
    if body.startswith("[Event]"):
        analyseMsg(body)

# TODO -> utiliser la fonction update_stock() une fois tout les jours ?
# La fonction check si la date d'aujourd'hui est incluse dans l'intervalle de date de l'event 
# Et met à jour le stock en conséquence

def analyseMsg(body: str):
    newBody = body.split("{", 1)[1]
    newBody = "{" + newBody
    newBody = newBody.replace("\'", "\"")
    event_dict = json.loads(newBody)
    event = _event(**event_dict)
    if event.location["address"] == "distanciel" or event.name == "Concours Puissance Alpha":
        # Besoin de rien
        return True
    elif event.name.find("CKoi1Ingé") != -1:
        # Besoin du matériel CKoi1Ingé + plaquettes + kakémono générique + goodies
        reserve_items(event = event, type="Kakémonos", label="Ingé/Bachelors", nbr=1)
        reserve_items(event = event, type="Brochures", label="FISE", nbr=event.contact_objective or 12)
        reserve_items(event = event, type="Goodies", label="Règles", nbr=event.contact_objective or 12)
        return True
    elif (event.name.lower().find("journée portes ouvertes") != -1) or (event.name.lower().find("jpo") != -1) or (event.name.lower().find("soirée portes ouvertes") != -1) or (event.name.lower().find("spo") != -1):
        # Besoin des kakémonos (VE, Ingé, Bachelor, CIN, BIOST, International, Génériques) + plaquettes + goodies
        # reserve_items(event = event, label="Goodies", nbr=event.contact_objective)
        # reserve_items(event = event, type="Kakémonos", label="Vie Etudiante", nbr=event.contact_objective)
        update_stock(event, "Kakémonos", "Ingé/Bachelors", event.contact_objective)
        # reserve_items(event = event, type="Kakémonos", label="Ingé/Bachelors", nbr=event.contact_objective)
        # reserve_items(event = event, type="Kakémonos", label="CIN", nbr=event.contact_objective)
        # reserve_items(event = event, type="Kakémonos", label="BIOST", nbr=event.contact_objective)
        # reserve_items(event = event, label="FISE", nbr=event.contact_objective)
        return True
    elif event.name.find("Retour lycée") != -1 or event.name.find("Intervention devant classe") != -1:
        # Besoin de plaquettes
        reserve_items(event = event, label="FISE",nbr=event.contact_objective or 50)
        update_stock(event, type = "Brochures", label = "FISE", nbr = event.contact_objective)
        return True
    elif event.name.find("Accueil lycée") != -1:
        # Besoin des kakémonos (Générique et Chiffres clés) + plaquettes + goodies sans sac
        reserve_items(event = event, type="Kakémonos", label="Ingé/Bachelors", nbr=1)
        reserve_items(event = event, type="Kakémonos", label="2 campus", nbr=1)
        reserve_items(event = event, label="Goodies", nbr=event.contact_objective or 25)
        return True
    elif event.name.lower() == "préparation":
        reserve_items(event = event, label="Goodies", nbr=event.contact_objective or 50)
        return True
    elif event.name.lower().find("remise des diplômes") != -1 or event.name.lower().find("remise des diplomes") != -1:
        # Besoin des kakémonos + lettres + bâches + chaises longues + identification sièges réservées
        reserve_items(event = event, label="Lettres", nbr=1)
        reserve_items(event = event, label="RDD", nbr=1)
        reserve_items(event = event, label="Transats", nbr=4)
        return True
    else:
        # Besoin des kakémonos en fonction de la taille du stand + plaquettes + goodies + bâches
        # reserve_items(event = event, type="Goodies", label="Stylos", nbr=event.contact_objective)
        # reserve_items(event = event, label="FISE", nbr=event.contact_objective or 100)
        # reserve_items(event = event, label="Puissance Alpha Générale", nbr=event.contact_objective or 100)
        # reserve_items(event = event, label="Kakémonos", nbr=int(event.contact_objective/3) or 33)
        return True


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, alert, sender, receiver, role="Responsable"):
    msg = MIMEMultipart('alternative')

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # Create the HTML version of your message
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
    


if __name__ == "__main__":
    
    # for _ in range(3):
    #     send_email("test", "test", "alex.olivier@isen.yncrea.fr", "marc.etavard@isen.yncrea.fr")    
    events = urllib_to_json(urllib.request.urlopen("http://localhost:5000/event/getAll"))
    for e in events:
        checkMsg(f"[Event]{e}")