#import dispensor.dispatcher
from dispensor.message import Message
from dispensor.message import Record
from dispensor.vector_clock import vector_clock_factory
from dispensor.dispatcher import dispatch

import requests
import socket
import threading

class UDPHost:
    def __init__(self, credentials, receiver):
        self.host, self.port = credentials
        self.receiver = receiver

    def credentials(self):
        print("here")
        return (self.host, self.port)

    def unicast(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(data, (self.host, self.port))

    def serve(self):
        def serve_forever():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind((self.host, self.port))
                while True:
                    data, addr = s.recvfrom(1400)
                    self.receiver.receive(data)

        self.thread = threading.Thread(target=serve_forever)
        self.thread.start()

class Host:
    def __init__(self, credentials, \
            group, \
            clock_factory=vector_clock_factory,
            concrete_host=UDPHost):
        #self.host, self.port = credentials
        self.thread = None
        self.clock_factory = clock_factory
        self.clock = self.clock_factory.empty_clock(credentials) 
        self.record = set()
        self.group = group
        self.group.add(self)
        self.concrete_host= \
                concrete_host(credentials,self)

        self.concrete_host.serve()

    def credentials(self):
        return self.concrete_host.credentials()

    def unicast(self, data):
        self.concrete_host.unicast(data)

    def multicast(self, data):
        for h in self.group:
            h.unicast(data)

    def receive(self, data):
        m = Message().unpack(data)
        clock = self.clock_factory.make_clock(m.clock, m.credentials)

        if not m in self.record:
            if tuple(m.credentials) \
                != tuple(self.credentials()):
                self.multicast(m.data)
        self.record.add(m)
        self.clock.update(clock)
        dispatch(m.clock, m.payload)




