from datetime import datetime, timedelta
from os import abort
import urllib.request, urllib.parse
import json
import os
from dotenv import load_dotenv
from messaging import urllib_to_json

load_dotenv()
api_event = os.getenv('API_EVENT')
api_stock = os.getenv('API_STOCK')


def reserve_item(event, type: str = "", label: str = "", nbr: int = 0):
    """
    Fonction qui sert à réserver un item pour un évènement donné 
    """
    item = find_item(name=label, type=type)  
    item_location_id = item["id"]
    actual_stock = item["quantity"]

    reserve_request = {
        "eventId": event.id,
        "item_locationId": item_location_id,
        "quantity": nbr,
    }
    overlapping = get_overlapping_events(event)
    if nbr > actual_stock:
        #TODO Alerte Stock insufisant
        pass

    predicted = 0        
    i = 0
    if overlapping != []:
        for e in overlapping:
            if e["id"] != event.id:
                reserved_items = urllib_to_json(urllib.request.urlopen(f"{api_stock}/reservedItem/getAll/{event.id}"))
                predicted+=reserved_items[i]["quantity"]
                i+=1
  
    if actual_stock - predicted < nbr:
        #TODO Alerte Stock insufisant
        pass
    data = urllib.parse.urlencode(reserve_request).encode()
    req =  urllib.request.Request(f"{api_stock}/reserveItem", data=data, method="POST")
    # resp_reserved = urllib.request.urlopen(req)

    return 0

def get_overlapping_events(event):
    """
    Fonction qui sert à vérifier si les dates de début et de fin d'un évènement
    dont la logistique est encore à faire chevauchent un autre évènement
    Lorsque la logistique d'un évènement a été effectuée, le matériel n'est pas disponible entre
    la date de début - 2j et de fin + 1j
    Renvoie la liste des événements qui chevauchent l'événement donné
    """
    overlapping_events = []

    if event.status["label"] == "A faire":
        events = urllib_to_json(urllib.request.urlopen(f"{api_event}/getAll"))

        date_start = datetime.strptime(event.date_start, '%a, %d %b %Y %H:%M:%S %Z')
        date_end = datetime.strptime(event.date_end, '%a, %d %b %Y %H:%M:%S %Z')
        date_interval = [date_start - timedelta(days=2), date_end + timedelta(days=1)]
        
        for e in events:
            if e["id"] == event.id:
                continue
            e_start = datetime.strptime(e["date_start"], '%a, %d %b %Y %H:%M:%S %Z') - timedelta(days=2)
            e_end = datetime.strptime(e["date_end"], '%a, %d %b %Y %H:%M:%S %Z') + timedelta(days=1)
            if (date_interval[0] <= e_end and date_interval[0] >= e_start) or (date_interval[1] <= e_end and date_interval[1] >= e_start):
                overlapping_events.append(e)
    return overlapping_events


def find_item(name: str = "", type:str = ""):
    materials = urllib_to_json(urllib.request.urlopen(f"{api_stock}/item/getAll"))
    for material in materials:
        if material["item_id"]["name"] == name and material["item_id"]["category_id"]["label"] == type:
            return material
        elif material["item_id"]["name"] == name:
            return material
    return 0


def update_stock(event, label, type, nbr):
    item = find_item(name=label, type=type)
    item_id = item["item_id"]["id"]
    location_id = item["location_id"]["id"]
    actual_stock = item["quantity"]
    quantity_ret = item["quantity_ret"] if "quantity_ret" in item else -1 
    # si quantity_ret pas specifiée
    category = item["item_id"]["category_id"]["label"]

    today = datetime.now()
    date_start = datetime.strptime(event.date_start, '%a, %d %b %Y %H:%M:%S %Z')
    date_end = datetime.strptime(event.date_end, '%a, %d %b %Y %H:%M:%S %Z')
    date_start = (date_start - timedelta(days=2))
    date_end = (date_end + timedelta(days=1))

    if today == date_start and actual_stock >= nbr:
        update_stock = {
            "name": label,
            "quantity": actual_stock - nbr,
            "location.id": location_id,
            "category": category,
        }
        data = urllib.parse.urlencode(update_stock).encode()
        req =  urllib.request.Request(f"{api_stock}/item/{item_id}/{location_id}", data=data, method="PUT")
        resp = urllib.request.urlopen(req)
    elif today == date_start and actual_stock <= nbr:
        # Alerte stock insuffisant
        abort(400, "Erreur lors de la réservation des items, quantité insuffisante")
    elif quantity_ret != -1 and today == date_end and event.status["label"] == "Fini":
        update_stock = {
            "name": label,
            "quantity": actual_stock + quantity_ret,
            "location.id": location_id,
            "category": category,
        }
        gain = (quantity_ret / nbr) * 100 # TODO
        data = urllib.parse.urlencode(update_stock).encode()
        req =  urllib.request.Request(f"{api_stock}/item/{item_id}/{location_id}", data=data, method="PUT")
        resp = urllib.request.urlopen(req)
    return 0


def minimal_stock(event, type, label):
    """
    Fonction qui définit le minimum de matériel nécessaire en fonction
    du nom et de la catégorie de l'item pour ne pas avoir d'alertes
    """
    if type == "Brochures" or type == "Goodies":
        return 100
    elif type == "Kakémonos":
        return 1
    elif type == "Feuilles" and (label == "Labyrinthe" or label == "Blanches" or label == "Ckoi1Ingé"):
        return 3
    elif type == "Médailles" and label == "Crayon" or label == "Ingé Quizz":
        return 3
    elif type == "Tablettes" and ((event.name.lower().find("journée portes ouvertes") != -1) or (event.name.lower().find("jpo") != -1)):
        return 5
    elif type == "Tablettes" and ((event.name.lower().find("soirée portes ouvertes") != -1) or (event.name.lower().find("spo") != -1)):
        return 2
    