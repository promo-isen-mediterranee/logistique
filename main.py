from customTypes import _event
from controller import urllib_to_json, check_dates_event
import urllib.request
import json
from controller import reserve_items

def checkMsg(body: str):
    if body.startswith("[Event]"):
        analyseMsg(body)


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
        reserve_items(event = event, label="Goodies", nbr=event.contact_objective)
        reserve_items(event = event, type="Kakémonos", label="Vie Etudiante", nbr=event.contact_objective)
        # reserve_items(event = event, type="Kakémonos", label="Ingé/Bachelors", nbr=event.contact_objective)
        # reserve_items(event = event, type="Kakémonos", label="CIN", nbr=event.contact_objective)
        # reserve_items(event = event, type="Kakémonos", label="BIOST", nbr=event.contact_objective)
        # reserve_items(event = event, label="FISE", nbr=event.contact_objective)
        return True
    elif event.name.find("Retour lycée") != -1 or event.name.find("Intervention devant classe") != -1:
        # Besoin de plaquettes
        reserve_items(event = event, label="FISE",nbr=event.contact_objective or 50)
        return True
    elif event.name.find("Accueil lycée") != -1:
        # Besoin des kakémonos (Générique et Chiffres clés) + plaquettes + goodies sans sac
        reserve_items(event = event, type="Kakémonos", label="Ingé/Bachelors", nbr=1)
        reserve_items(event = event, type="Kakémonos", label="2 campus", nbr=1)
        reserve_items(event = event, type="Goodies", nbr=event.contact_objective or 25)
        return True
    elif event.name.lower() == "préparation":
        reserve_items(event = event, type="Goodies", nbr=event.contact_objective or 50)
        return True
    elif event.name.lower().find("remise des diplômes") != -1 or event.name.lower().find("remise des diplomes") != -1:
        # Besoin des kakémonos + lettres + bâches + chaises longues + identification sièges réservées
        reserve_items(event = event, type="Lettres", nbr=1)
        reserve_items(event = event, type="RDD", nbr=1)
        reserve_items(event = event, type="Transats", nbr=4)
        return True
    else:
        # Besoin des kakémonos en fonction de la taille du stand + plaquettes + goodies + bâches
        # reserve_items(event = event, type="Goodies", label="Stylos", nbr=event.contact_objective)
        # reserve_items(event = event, label="FISE", nbr=event.contact_objective or 100)
        # reserve_items(event = event, label="Puissance Alpha Générale", nbr=event.contact_objective or 100)
        # reserve_items(event = event, label="Kakémonos", nbr=int(event.contact_objective/3) or 33)
        return True


if __name__ == "__main__":
    events = urllib_to_json(urllib.request.urlopen("http://localhost:5000/event/getAll"))
    for e in events:
        checkMsg(f"[Event]{e}")