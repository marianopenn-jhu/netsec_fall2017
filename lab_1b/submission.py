#Mariano Pennini
#Network Security Fall 2017
#Assignment 1b

from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import BOOL, UINT32, STRING
import unittest

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

class UnitTest(unittest.TestCase):

    #Test request flip packet
    def test1(self):
        flipPacket = RequestFlip()
        flipPacket.headOrTail = True
        flipPacket.numFlips = 10
        packetBytes = flipPacket.__serialize__()
        flipPacketDes = PacketType.Deserialize(packetBytes)
        assert flipPacket == flipPacketDes

    #Test request flip packet with bad numFlips value
    def test2(self):
        flipPacket = RequestFlip()
        flipPacket.headOrTail = True
        with self.assertRaises(ValueError):
            flipPacket.numFlips = -10.5

    #Test winner packet
    def test3(self):
        winnerPacket = CurrentWinner()
        packetBytesWinner = winnerPacket.__serialize__()
        winnerPacketDes = PacketType.Deserialize(packetBytesWinner)
        assert winnerPacket == winnerPacketDes

    #Test flip result packet
    def test4(self):
        flipResult = FlipResult()
        flipResult.successOrFailure = True
        flipResult.observedFrequency = "51%"
        flipResPacketBytes = flipResult.__serialize__()
        flipResultPacketDes = flipResult.Deserialize(flipResPacketBytes)
        assert flipResult == flipResultPacketDes

if __name__ == '__main__':
    unittest.main()
