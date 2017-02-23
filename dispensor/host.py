from dispensor.message import Message
from dispensor.message import Record
from dispensor.vector_clock import vector_clock_factory
from dispensor.dispatcher import dispatch

class Host:
    def __init__(self, \
            concrete_host, \
            group, \
            clock_factory=vector_clock_factory):
        #self.host, self.port = credentials
        self.thread = None
        self.clock_factory = clock_factory
        self.clock = self.clock_factory.empty_clock(group.me) 
        self.record = set()
        self.group = group
        self.concrete_host = concrete_host
        self.concrete_host.receiver = self

        self.concrete_host.serve()

    def credentials(self):
        return self.concrete_host.credentials()

    def unicast_(self, h, data):
        self.concrete_host.unicast(h, data)

    def multicast_(self, data):
        for h in self.group:
            self.unicast_(h, data)

    def multicast(self, payload):
        m = Message().pack(self.clock.to_message(), \
                self.credentials(), payload)
        self.multicast_(m.data)

    def unicast(self, cred, payload):
        m = Message().pack(self.clock.to_message(), \
                self.credentials(), payload)
        self.unicast_(m.data)

    def receive(self, data):
        m = Message().unpack(data)
        clock = self.clock_factory.make_clock(m.clock, m.credentials)

        if not m in self.record:
            if tuple(m.credentials) \
                != tuple(self.credentials()):
                self.multicast_(m.data)
        self.record.add(m)
        self.clock.update(clock)
        dispatch(m.clock, m.payload)




