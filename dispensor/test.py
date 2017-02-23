import dispensor.host
import dispensor.udp
import dispensor.group
import time

c = dispensor.udp.UDPHost('localhost', 23412)
g = dispensor.group.Group(c)
h = dispensor.host.Host(c, g)

print("creds", h.credentials())

time.sleep(1)
h.multicast("hello world")
