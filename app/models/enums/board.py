from enum import Enum


class BoardStatus(str, Enum):
    active = "active"
    archived = "archived"
    deleted = "deleted"


class CardState(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    in_review = "in_review"
    done = "done"


class UserRoleType(str, Enum):
    owner = "owner"
    member = "member"
