class Host:
    def __init__(self,name,port):

    def addPort(self):
        return

    def send(self):
        return

class Router(algorith?):
    def __init__(self):
        self.queue = []

    def receivePacket(packet)

class Packet:
    def __init__(self,destination,information):
        self.destination = destination
        self.information = information
        self.size = len(information)

class Link:
    def __init__():
        self.capacity = 0

    def receivePacket(packet):
        # wait the amount of time it would take to transmit the packet
        # add the packet to the Link

#where do we 'store' the packets which are waiting in the link...?
#consensus is that we will store it in the link
"""
A -L1-> R1 -L2-> R2 -L3-> B
At any given time the packet is owned by one of the objects above

A gives packet to L1
L1 gives packet to R1
R1 gives packets to L2... etc

packet = Packet(...)
A.send(packet) information in packet directs it to L1
"""
