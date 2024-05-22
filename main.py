from customTypes import _event
import urllib.request
import json
from controller import reserve_items

def urllib_to_json(byte_obj):
    events = byte_obj.read()
    encoding = byte_obj.info().get_content_charset('utf-8')
    JSON_object = json.loads(events.decode(encoding))
    return JSON_object

def checkMsg(body: str):
    if body.startswith("[Event]"):
        analyseMsg(body)


def analyseMsg(body: str):
    newBody = body.split("{", 1)[1]
    newBody = "{" + newBody
    newBody = newBody.replace("\'", "\"")
    event_dict = json.loads(newBody)
    event = _event(**event_dict)
    print(event)
    #materials = urllib.request.urlopen("http://promo-api.prinv.isen.fr/stock/items/getAll").read()
    materials = urllib.request.urlopen("http://localhost:5100/stock/item/getAll").read()
    if event.location["address"] == "distanciel" or event.name == "Concours Puissance Alpha":
        # Besoin de rien
        return True
    elif event.name.find("CKoi1Ingé"):
        # Besoin du matériel CKoi1Ingé + plaquettes + kakémono générique + goodies
        reserve_items(type="Brochures", label="FISE", nbr=event.contact_objective or 12)
        reserve_items(type="Goodies", nbr=event.contact_objective or 12)
        return True
    elif event.name.lowerCase.find("journée portes ouvertes") | event.name.lowerCase.find("jpo") | event.name.lowerCase.find("soirée portes ouvertes") | event.name.lowerCase.find("spo"):
        # Besoin des kakémonos (VE, Ingé, Bachelor, CIN, BIOST, International, Génériques) + plaquettes + goodies
        reserve_items(type="Goodies", nbr=event.contact_objective)
        reserve_items(type="", nbr=event.contact_objective)
        return True
    elif event.name.find("Retour lycée") | event.name.find("Intervention devant classe"):
        # Besoin de plaquettes
        reserve_items(label="FISE",nbr=event.contact_objective or 50)
        return True
    elif event.name.find("Accueil lycée"):
        # Besoin des kakémonos (Générique et Chiffres clés) + plaquettes + goodies sans sac
        reserve_items(type="Kakémonos", label="Ingé/Bachelors", nbr=1)
        reserve_items(type="Kakémonos", label="2 campus", nbr=1)
        reserve_items(type="Goodies", nbr=event.contact_objective or 25)
        return True
    elif event.name.lowerCase == "préparation":
        reserve_items(type="Goodies", nbr=event.contact_objective or 50)
        return True
    elif event.name.lowerCase.find("remise des diplômes") | event.name.lowerCase.find("remise des diplomes"):
        # Besoin des kakémonos + lettres + bâches + chaises longues + identification sièges réservées
        reserve_items(type="Lettres", nbr=1)
        reserve_items(type="RDD", nbr=1)
        reserve_items(type="Transats", nbr=4)
        return True
    else:
        # Besoin des kakémonos en fonction de la taille du stand + plaquettes + goodies + bâches
        reserve_items(type="Goodies", nbr=event.contact_objective)
        reserve_items(label="FISE", nbr=event.contact_objective or 100)
        reserve_items(label="Puissance Alpha", nbr=event.contact_objective or 100)
        reserve_items(label="", nbr=event.contact_objective/3 or 33)
        return True
    return False

if __name__ == "__main__":
    events = urllib_to_json(urllib.request.urlopen("http://localhost:5000/event/getAll"))
    for e in events:
        checkMsg(f"[Event]{e}")