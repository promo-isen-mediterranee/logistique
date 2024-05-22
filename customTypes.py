from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class _status:
    """
    A class representing a status.

    Attributes:
        id: Id of the status
        label: Label of the status
    """
    id: int
    label: str

@dataclass
class _itemManager:
    """
    A class representing an item manager.

    Attributes:
        id: Id of the item manager
        first_name: First name of the item manager
        last_name: Last name of the item manager
    """
    id: str
    first_name: str
    last_name: str

@dataclass
class _location:
    """
    A class representing a location.

    Attributes:
        id: Id of the location
        address: Address where the location will take place
        city: The city where the location is
        room: The room label, if this location is for a room
    """
    id: int
    address: str
    city: str
    room: Optional[str] = None

@dataclass
class _event:
    """
    A class representing an event.

    Attributes:
        id: Id of the event
        name: Name of the event
        stand_size: Size of a stand, if available
        contact_objective: Goal number of contacts to collect during the event, if available
        date_start: Date Time of the start of the event
        date_end: Date Time of the end of the event
        status: Status of the event
        item_manager: Details of the person who brings the items onto the event
        location: Where the event will take place
    """
    id: int
    name: str
    date_start: datetime
    date_end: datetime
    status: _status
    item_manager: _itemManager
    location: _location
    stand_size: Optional[int] = None
    contact_objective: Optional[int] = None

@dataclass
class _category:
    """
    A class representing a category.

    Attributes:
        id: Id of the category
        label: Category of the item
    """
    id: int
    label: str

@dataclass
class _item:
    """
    A class representing an item.

    Attributes:
        id: Id of the item
        name: Name of the item
        category: Category of the item
    """
    id: int
    name: str
    category: _category

@dataclass
class _stockItem:
    """
    A class representing a stocked item.

    Attributes:
        item: Item corresponding to this stocked item
        location: Where this stocked item is located
        quantity: The quantity of this item
    """
    item: _item
    location: _location
    quantity: int