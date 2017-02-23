import dispensor.udp
import dispensor.message
import dispensor.group
import time

me = ('localhost', 23412)

g = dispensor.group.Group(me)
h = dispensor.udp.Host(me, g)

print("creds", h.credentials())

time.sleep(1)
h.multicast("hello world")
