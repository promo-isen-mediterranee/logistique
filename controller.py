from datetime import datetime, timedelta
from os import abort
import urllib.request, urllib.parse
import json


def urllib_to_json(byte_obj):
    events = byte_obj.read()
    encoding = byte_obj.info().get_content_charset('utf-8')
    JSON_object = json.loads(events.decode(encoding))
    return JSON_object

def reserve_items(event, type: str = "", label: str = "", nbr: int = 0):
    """
    Fonction qui sert à réserver tout les items pour un évènement donné 
    et mettre le stock à jour en conséquence
    """

    item = find_item(name=label, type=type)  
    item_location_id = item["id"]

    reserve_request = {
        "eventId": event.id,
        "item_locationId": item_location_id,
        "status": True,
        "quantity": nbr,
    }
    data = urllib.parse.urlencode(reserve_request).encode()
    req =  urllib.request.Request("http://localhost:5100/stock/reserveItem", data=data, method="POST")
    resp_reserved = urllib.request.urlopen(req)


def check_dates_event(event):
    """
    Fonction qui sert à vérifier si les dates de début et de fin d'un évènement
    dont la logistique est encore à faire chevauchent un autre évènement
    Lorsque la logistique d'un évènement a été effectuée, le matériel n'est pas disponible entre
    la date de début - 2j et de fin + 1j
    """
    if event.status["label"] == "A faire":
        events = urllib_to_json(urllib.request.urlopen("http://localhost:5000/event/getAll"))

        date_start = datetime.strptime(event.date_start, '%Y-%m-%d') #%H:%M')
        date_end = datetime.strptime(event.date_end, '%Y-%m-%d')

        date_interval = (date_start - timedelta(days=2), date_end + timedelta(days=1))
        for e in events:
            if e["date_start"] in date_interval:
                return 1
    return 0


def find_item(materials, name: str = "", type:str = ""):
    # materials = urllib_to_json(urllib.request.urlopen("http://promo-api.prinv.isen.fr/stock/items/getAll"))
    materials = urllib_to_json(urllib.request.urlopen("http://localhost:5100/stock/item/getAll"))
    for material in materials:
        if material["item_id"]["name"] == name and material["item_id"]["category_id"]["label"] == type:
            return material
        elif material["item_id"]["name"] == name:
            return material
    return 0


def update_stock(event, label, type, nbr):
    overlapping = check_dates_event(event)

    item = find_item(name=label, type=type)
    item_id = item["item_id"]["id"]
    location_id = item["location_id"]["id"]
    actual_stock = item["quantity"]
    category = item["item_id"]["category_id"]["label"]

    today = datetime.now().date()
    date_start = datetime.strptime(event.date_start, '%Y-%m-%d')#%H:%M')
    date_end = datetime.strptime(event.date_end, '%Y-%m-%d')
    date_interval = (date_start - timedelta(days=2), date_end + timedelta(days=1))
    today_in_interval = (date_interval[0].date() <= today <= date_interval[1].date())

    if not overlapping and today_in_interval and actual_stock >= nbr:
        update_stock = {
            "name": label,
            "quantity": actual_stock - nbr,
            "location.id": location_id,
            "category": category,
        }
        data = urllib.parse.urlencode(update_stock).encode()
        req =  urllib.request.Request(f"http://localhost:5100/stock/item/{item_id}/{location_id}", data=data, method="PUT")
        resp = urllib.request.urlopen(req)
    else:
        abort(400, "Erreur lors de la réservation des items, quantité insuffisante ou date invalide")
    return True