import os
from datetime import datetime, timedelta
from messaging import send_email_to_role, send_request

api_event = os.getenv('API_EVENT')

def ValidateEvent():
    event = send_request(f"{api_event}/getAll")    
    for e in event:
        if e['status']['label'] == "A faire":
            e_date = datetime.strptime(e['date_start'], '%a, %d %b %Y %H:%M:%S %Z')
            print(f"Event : {e['name']}", (e_date).date())
            if datetime.now().date() == (e_date - timedelta(days=7)).date():
                send_email_to_role("Alerte : Evènement imminent, 7 jours restants !", 
                                f"L'évènement {e['name']} commence dans 7 jours, veuillez finir la logistique au plus vite !")
            elif datetime.now().date() == (e_date - timedelta(days=5)).date():
                send_email_to_role("Alerte : Evènement imminent, 5 jours restants !", 
                                f"L'évènement {e['name']} commence dans 5 jours, veuillez finir la logistique au plus vite !")
            elif datetime.now().date() == (e_date - timedelta(days=3)).date():
                send_email_to_role("Alerte : Evènement imminent, 3 jours restants !", 
                                f"L'évènement {e['name']} commence dans 3 jours, veuillez finir la logistique au plus vite !")
            elif datetime.now().date() >= (e_date - timedelta(days=2)).date() and (0<=datetime.now().day - e_date.day):              
                send_email_to_role(f"Alerte : Evènement imminent, {datetime.now().day - e_date.day} jours et {(datetime.now().hour - e_date.hour)} heures restantes !", 
                                f"L'évènement {e['name']} commence dans {datetime.now().day - e_date.day} jours et {(datetime.now().hour - e_date.hour)} heures, veuillez finir la logistique au plus vite !")
                return True # à décommenter pour lancer l'alerte toutes les 2 heures si action non réalisée
    return False

# Si validateEvent retourne True, crée un fichier temporaire
if ValidateEvent():
    with open('/tmp/dead_line.tmp', 'w') as f:
        f.write('T')
else:
    with open('/tmp/dead_line.tmp', 'w') as f:
        f.write('F')
