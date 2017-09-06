#Mariano Pennini
#Network Security Fall 2017
#Assignment 1b

from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import BOOL, UINT32, STRING

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

def unitTest():

    flipPacket = RequestFlip()
    flipPacket.headOrTail = True
    flipPacket.numFlips = 10
    packetBytes = flipPacket.__serialize__()
    flipPacketDes = PacketType.Deserialize(packetBytes)
    assert flipPacket == flipPacketDes

    #Test Winner Packet
    winnerPacket = CurrentWinner()
    packetBytesWinner = winnerPacket.__serialize__()
    winnerPacketDes = PacketType.Deserialize(packetBytesWinner)
    assert winnerPacket == winnerPacketDes

    #Test flip result packet
    flipResult = FlipResult()
    flipResult.successOrFailure = True
    flipResult.observedFrequency = "51.0%"
    flipResPacketBytes = flipResult.__serialize__()
    flipResultPacketDes = flipResult.Deserialize(flipResPacketBytes)
    assert flipResult == flipResultPacketDes


if __name__ == '__main__':
    unitTest()
