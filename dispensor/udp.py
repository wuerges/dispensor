#import dispensor.dispatcher
from dispensor.message import Message
from dispensor.message import Record
from dispensor.vector_clock import vector_clock_factory
from dispensor.dispatcher import dispatch

import requests
import socket
import threading

class UDPHost:
    def __init__(self, credentials, \
            group, \
            clock_factory=vector_clock_factory):
        self.host, self.port = credentials
        self.thread = None
        self.clock_factory = clock_factory
        self.clock = self.clock_factory.empty_clock(credentials) 
        self.record = set()
        self.group = group
        self.group.add(self)

    def credentials(self):
        return (self.host, self.port)


    def serve(self):
        def serve_forever():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind((self.host, self.port))
                while True:
                    data, addr = s.recvfrom(1400)
                    self.receive(data)

        self.thread = threading.Thread(target=serve_forever)
        self.thread.start()

    def unicast(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            print("sending", data, self.host, self.port)
            s.sendto(data, (self.host, self.port))

    def multicast(self, data):
        for h in self.group:
            h.unicast(data)

    def receive(self, data):
        m = Message().unpack(data)
        clock = self.clock_factory.make_clock(m.clock, m.credentials)
        self.clock.update(clock)

        if not m in self.record:
            if tuple(m.credentials) \
                != tuple(self.credentials()):
                self.multicast(m.data)
        self.record.add(m)
        dispatch(m.clock, m.payload)




