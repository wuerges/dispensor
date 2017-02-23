import json

class Message:
    def __init__(self):
        pass

    def unpack(self, data):
        j = json.loads(data.decode())
        self.data = data
        self.clock = j['clock']
        self.credentials = j['credentials']
        self.payload = j['payload']
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

class Record:
    def __init__(self):
        self.record = set()

    def __contains__(self, m):
        return (m.clock, m.credentials) in self.record

    def add(self, m):
        self.record.add((m.clock, m.credentials))



