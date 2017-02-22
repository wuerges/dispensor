#import dispensor.dispatcher
from dispensor.message import Message
from dispensor.vector_clock import vector_clock_factory

import requests
import socket
import threading

class UDPHost:
    def __init__(self, credentials, \
            clock_factory=vector_clock_factory):
        self.host, self.port = credentials
        self.thread = None
        self.clock_factory = clock_factory

    def credentials(self):
        return (host, port)


    def serve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((self.host, self.port))

            def serve_forever():
                while True:
                    data, addr = s.recvfrom(1024)
                    self.receive(data)

            self.thread = threading.Thread(target=serve_forever)
            self.thread.start()

    def unicast(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(data, (self.host, self.port))

    def multicast(self, data, group):
        for h in group:
            h.unicast(data)

    def receive(self, data):
        m = Message().unpack(data)
        h = UDPHost(m.credentials)
        clock = self.clock_factory(m.clock, m.credentials)


