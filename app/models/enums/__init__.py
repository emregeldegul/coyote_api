from enum import Enum


class Status(str, Enum):
    active = "active"
    passive = "passive"
    deleted = "deleted"


class State(str, Enum):
    approved = "approved"
    waiting = "waiting"
    decline = "decline"
