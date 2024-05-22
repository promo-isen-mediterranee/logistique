from collections import namedtuple
import datetime
from typing import Optional

class _status(namedtuple):
    id: int
    label: str

    id.__doc__ = "Id of the status"
    label.__doc__ = "Label of the status"

class _itemManager(namedtuple):
    id: str
    first_name: str
    last_name: str

    id.__doc__ = "Id of the item manager"
    first_name.__doc__ = "First name of the item manager"
    last_name.__doc__ = "Last name of the item manager"

class _location(namedtuple):
    id: int
    address: str
    city: str
    room: Optional[str] = None

    id.__doc__ = "Id of the location"
    address.__doc__ = "Address where the location will take place"
    city.__doc__ = "The city where the location is"
    room.__doc__ = "The room label, if this location is for a room"

class _event(namedtuple):
    id: int
    name: str
    stand_size: Optional[int] = None
    contact_objective: Optional[int] = None
    date_start: datetime
    date_end: datetime
    status: _status
    item_manager: _itemManager
    location: _location

    id.__doc__ = "Id of the event"
    name.__doc__ = "Name of the event"
    stand_size.__doc__ = "Size of a stand, if available"
    contact_objective.__doc__ = "Goal number of contacts to collect during the event, if available"
    date_start.__doc__ = "Date Time of the start of the event"
    date_end.__doc__ = "Date Time of the end of the event"
    status.__doc__ = "Status of the event"
    item_manager.__doc__ = "Details of the person who brings the items onto the event"
    location.__doc__ = "Where the event will take place"

class _category(namedtuple):
    id: int
    label: str

    id.__doc__ = "Id of the category"
    label.__doc__ = "Category of the item"


class _item(namedtuple):
    id: int
    name: str
    category: _category

    id.__doc__ = "Id of the item"
    name.__doc__ = "Name of the item"
    category.__doc__ = "Category of the item"

class _stockItem(namedtuple):
    item: _item
    location: _location
    quantity: int

    item.__doc__ = "Item corresponding to this stocked item"
    location.__doc__ = "Where this stocked item is located"
    quantity.__doc__ = "The quantity of this item"