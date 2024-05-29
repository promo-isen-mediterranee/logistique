import os
from datetime import datetime, timedelta
from messaging import send_email_to_role, send_request

# Script pour envoyer des alertes par mail aux responsables d'évènements
#commandes Unix pour lancer le script
# configurer Cron : 
# sudo service cron start
# crontab -e
# 0 0 * * 1-5 /usr/bin/python3 [votre_répertoire]/scrypt_bot_alert.py && echo "Script ran successfully" || echo "Script failed"
# 0 */2 * * * [ -f /tmp/validate_event.tmp ] && /usr/bin/python3 [votre_répertoire]/scrypt_bot_alert.py && rm /tmp/validate_event.tmp

api_event = os.getenv('API_EVENT')


def ValidateEvent():
    event = send_request(f"{api_event}/getAll")
    print("Running ValidateEvent function")
    if event["status"] == "A faire":
        for e in event:
            if datetime.now().date() == (e["date_start"] - timedelta(days=7)).date():
                send_email_to_role("Alerte : Evènement imminent, 7 jours restants !", 
                                f"L'évènement {e['name']} commence dans 7 jours, veuillez finir la logistique au plus vite !")
            elif datetime.now().date() == (e["date_start"] - timedelta(days=5)).date():
                send_email_to_role("Alerte : Evènement imminent, 5 jours restants !", 
                                f"L'évènement {e['name']} commence dans 5 jours, veuillez finir la logistique au plus vite !")
            elif datetime.now().date() == (e["date_start"] - timedelta(days=3)).date():
                send_email_to_role("Alerte : Evènement imminent, 3 jours restants !", 
                                f"L'évènement {e['name']} commence dans 3 jours, veuillez finir la logistique au plus vite !")
            elif datetime.now().date() <= (e["date_start"] - timedelta(days=2)).date():                
                send_email_to_role("Alerte : Evènement imminent, 2 jours restants !", 
                                f"L'évènement {e['name']} commence dans 2 jours, veuillez finir la logistique au plus vite !")
                # return True # à décommenter pour lancer l'alerte toutes les 2 heures si action non réalisée
    return False

# Si validateEvent retourne True, crée un fichier temporaire
if ValidateEvent():
    with open('/tmp/validate_event.tmp', 'w') as f:
        f.write('True')

# Tests :
# * * * */3 * /usr/bin/python3 /mnt/c/Users/alexo/OneDrive/Cours/ISEN S8/Apps/PromoIsenInventory/API/Service_Logistique/scrypt_bot_alert.py && echo "Script ran successfully" || echo "Script failed"
# * * * */1 * [ -f /tmp/validate_event.tmp ] && /usr/bin/python3 /mnt/c/Users/alexo/OneDrive/Cours/ISEN\ S8/Apps/PromoIsenInventory/logistique/scrypt_bot_alert.py && rm /tmp/validate_event.tmp7