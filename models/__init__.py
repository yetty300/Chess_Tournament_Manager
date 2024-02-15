from .club import ChessClub
from .club_manager import ClubManager
from .player import Player

__all__ = ["Player", "ChessClub", "ClubManager"]


class PersonException(Exception):
    pass


class InvalidDOBPersonException(PersonException):
    pass


try:

    raise InvalidDOBPersonException("Invalid Date of Birth")

except PersonException:

    print("PersonException caught")

except InvalidDOBPersonException("Invalid Date of Birth"):

    print("InvalidDOBPersonException caught")

except Exception:

    print("Exception caught.")
