#Mariano Pennini
#Network Security Homework 1c

import asyncio
from enum import Enum
from playground import connection
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import BOOL, UINT32, STRING
from pennini_packets import RequestFlip, CurrentWinner, FlipResult, Face, REQUEST_ERROR
import random
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
import unittest
import logging

winner_record = {"FACE":Face.TIE, "HEAD": 0, "TAIL":0, "FLIPS":0}

class CoinServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self._deserializer = PacketType.Deserializer()

    def data_received(self, data):
        self._deserializer.update(data)
        print('---Data received and is being processed on the server.')
        for pkt in self._deserializer.nextPackets():
            if(isinstance(pkt,CurrentWinner)):
                response = FlipResult()
                currFace = winner_record["FACE"]
                response.successOrFailure = currFace
                response.observedFrequency = "-0.0"
                self.transport.write(PacketType.__serialize__(response))

            elif(isinstance(pkt, RequestFlip)):
                result = self.processFlip(pkt.headOrTail, pkt.numFlips)
                response = FlipResult()
                faceGuess = self.parseFace(pkt.headOrTail)
                winningFace = result[0]

                if faceGuess == winningFace:
                    response.successOrFailure = 1
                else:
                    response.successOrFailure = 0
                response.observedFrequency = str(float(result[1]) / float(pkt.numFlips))
                self.transport.write(PacketType.__serialize__(response))

            else:
                self.transport.write(REQUEST_ERROR)
        self.transport.write(bytes(winner_record["FLIPS"]))

    def parseFace(self, face):
        if face == 0:
            return Face.HEAD
        else:
            return Face.TAIL

    def processFlip(self, headOrTail, numFlips):
        tails = 0
        heads = 0
        for flip in range(numFlips):
            rand = random.randint(0,1)
            if rand:
                tails += 1
                winner_record["TAIL"] += 1
            else:
                heads +=1
                winner_record["HEAD"] +=1
            winner_record["FLIPS"]+=1
        if tails>heads:
            winner_record["FACE"] = Face.TAIL
            return (Face.TAIL, tails)
        elif heads>tails:
            winner_record["FACE"] = Face.HEAD
            return (Face.HEAD, heads)
        else:
            winner_record["FACE"] = Face.TIE
            return (Face.TIE, heads)

#loop = asyncio.get_event_loop()
#coro = loop.create_server(CoinServerProtocol, '127.0.0.1', 8888)
server = connection.getConnector().create_playground_server(CoinServerProtocol,8888)
