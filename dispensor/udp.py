import socket
import threading

class UDPHost:
    def __init__(self, host, port, message_length=1400):
        self.host = host
        self.port = port
        self.receiver = None
        self.message_length = message_length

    def credentials(self):
        return (self.host, self.port)

    def unicast(self, cred, data):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(data, cred)

    def serve(self):
        def serve_forever():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind((self.host, self.port))
                while True:
                    data, addr = s.recvfrom(self.message_length)
                    self.receiver.receive(data)

        self.thread = threading.Thread(target=serve_forever)
        self.thread.start()

