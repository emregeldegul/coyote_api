from random import choices
from string import ascii_uppercase, digits


def generate_verification_code(length: int = 50):
    return "".join(choices(ascii_uppercase + digits, k=length))
