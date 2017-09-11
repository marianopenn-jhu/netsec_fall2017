#Mariano Pennini
#Network Security Homework 1c

from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import BOOL, UINT32, STRING
from enum import Enum

REQUEST_ERROR = "Invalid request. Check request data and try again."

class Face(Enum):
    HEAD = 0
    TAIL = 1
    TIE = -1

class RequestFlip(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.mpennin3.RequestFlip"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
            ("headOrTail", BOOL),
            ("numFlips", UINT32)
            ]

class CurrentWinner(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.mpennin3.CurrentWinner"
    DEFINITION_VERSION = "1.0"

    FIELDS = []

class FlipResult(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.mpennin3.FlipResult"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
            ("successOrFailure", BOOL),
            ("observedFrequency", STRING)
            ]
