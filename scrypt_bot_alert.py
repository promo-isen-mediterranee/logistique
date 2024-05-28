import os
import urllib.request
from datetime import datetime, timedelta
from messaging import send_email_to_role, urllib_to_json


#commandes Unix pour lancer le script
# configurer Cron : 
# sudo service cron start
# crontab -e
# 0 0 * * 1-5 /usr/bin/python3 [votre_répertoire]/scrypt_bot_alert.py && echo "Script ran successfully" || echo "Script failed"
# 0 */2 * * * [ -f /tmp/validate_event.tmp ] && /usr/bin/python3 [votre_répertoire]/scrypt_bot_alert.py && rm /tmp/validate_event.tmp

api_event = os.getenv('API_EVENT')


def ValidateEvent():
    event = urllib_to_json(urllib.request.urlopen(f"{api_event}/getAll"))
    if event["status"] == "A faire":
        if event["date_start"] == datetime.now() - timedelta(days=7):
            send_email_to_role("Alerte : Evènement imminent, 7 jours restants !", 
                               f"L'évènement {event['name']} commence dans 7 jours, veuillez finir la logistique au plus vite !")
        elif event["date_start"] == datetime.now() - timedelta(days=5):
            send_email_to_role("Alerte : Evènement imminent, 5 jours restants !", 
                               f"L'évènement {event['name']} commence dans 5 jours, veuillez finir la logistique au plus vite !")
        elif event["date_start"] == datetime.now() - timedelta(days=3):
            send_email_to_role("Alerte : Evènement imminent, 3 jours restants !", 
                               f"L'évènement {event['name']} commence dans 3 jours, veuillez finir la logistique au plus vite !")
        elif event["date_start"] == datetime.now() - timedelta(days=2):
            send_email_to_role("Alerte : Evènement imminent, 2 jours restants !", 
                               f"L'évènement {event['name']} commence dans 2 jours, veuillez finir la logistique au plus vite !")
            # return True # à décommenter pour lancer l'alerte toutes les 2 heures si action non réalisée
    return False

# Si validateEvent retourne True, crée un fichier temporaire
if ValidateEvent():
    with open('/tmp/validate_event.tmp', 'w') as f:
        f.write('True')

# 0 0 * * 1-5 /usr/bin/python3 /mnt/c/Users/alexo/OneDrive/Cours/ISEN\ S8/Apps/PromoIsenInventory/logistique/scrypt_bot_alert.py && echo "Script ran successfully" || echo "Script failed"
# 0 */2 * * * [ -f /tmp/validate_event.tmp ] && /usr/bin/python3 /mnt/c/Users/alexo/OneDrive/Cours/ISEN\ S8/Apps/PromoIsenInventory/logistique/scrypt_bot_alert.py && rm /tmp/validate_event.tmp