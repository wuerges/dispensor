import dispensor.udp
import dispensor.message
import time

me = ('localhost', 23412)

h = dispensor.udp.UDPHost(me, set())

m = dispensor.message.Message().pack({}, me, "hello world")


h.serve()

print(h.credentials())

time.sleep(1)
h.multicast(m.data)
