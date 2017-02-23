import socket
import threading

class UDPHost:
    def __init__(self, credentials, receiver):
        self.host, self.port = credentials
        self.receiver = receiver

    def credentials(self):
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

