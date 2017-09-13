import asyncio
from enum import Enum
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import BOOL, UINT32, STRING
from pennini_packets import RequestFlip, CurrentWinner, FlipResult, Face, REQUEST_ERROR
import random
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
import unittest
import logging

class CoinClientProtocol(asyncio.Protocol):
    def __init__(self, data):
        self.requestPacket = data
        self._deserializer = PacketType.Deserializer()
        self.transport = None

    def parseFace(self, face):
        if face == 0:
            return Face.HEAD
        else:
            return Face.TAIL

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.requestPacket.__serialize__())
        print('---Data sent on client: {!r}'.format(self.requestPacket))

    def data_received(self, data):
        self._deserializer.update(data)
        print('---Data received on the client.')
        for pkt in self._deserializer.nextPackets():
            if isinstance(pkt, FlipResult) and (pkt.observedFrequency == "-0.0"):
                print('Last winning face was {!r}'.format(self.parseFace(pkt.successOrFailure)))
            elif(isinstance(pkt,FlipResult)):
                if pkt.successOrFailure:
                    print('You guessed correctly!')
                elif (pkt.successOrFailure) == 0:
                    print('Sorry, you guessed the wrong face!')
                print('Observed frequency of winning face: {!r}'.format(pkt.observedFrequency))


    def connection_lost(self, exc):
        self.transport = None
        print('---The server closed the connection')
        print('---Stop the event loop')
        self.loop.stop()
