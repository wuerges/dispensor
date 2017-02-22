import json

class Message:
    def __init__(self):
        pass

    def unpack(self, data):
        j = json.loads(data.decode())
        self.data = data
        self.clock = j.clock
        self.credentials = j.clock
        self.payload = j.payload
        return self
    
    def pack(self, clock, credentials, payload):
        j = json.dumps({'clock': clock, \
                'credentials': credentials, \
                'payload': payload })
        self.data = j.encode()
        self.clock = clock
        self.credentials = credentials
        self.payload = payload
        return self

