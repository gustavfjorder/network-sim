AWKNOWLEDGEMENT_PACKET_SIZE = 64
# may assume that acknowledgement packets have a fixed size of 64 bytes.
FLOW_GENERATED_PACKET_SIZE = 1024
# may assume that flow-generated data packets have a fixed size of 1024 bytes,
# including any packet headers or trailers

# For queue in Link
import collections

# By default, if a function has a yield statement in it, it is a generator.

# Note: For acknowledgements, we should be saying I'm expecting this packet next
# instead of saying I just received this packet
# packet 1 received. ACK: expecting packet 2 next.
# Sorry, above is only true for Tahoe, and different for Reno
# need to discuss this. Look at page 92 of WP
class Host:
    def __init__(self,env,name,port):
        self.env = env
        self.id = name
        addLink(link)
        self.flows = []

    def addFlow(flow):
        self.flows.append(flow)

    def addLink(link):
        self.link = link

    def send(self, packet):
        # From flow to link
        self.link.put(packet)
        return

    def put(self, packet):
        # Receive a packet from link
        # Pass it to flow
        # receive ack OR send ack if it isn't an ack
        if(packet.type == 'ACK'):
            pass
        else:
            # Packet is not an Awknoledgement, need to  send an awknowledgement
            # new destination is the source, get this from the flow
        pass

    def run(self):
        while (True):
            # if there is a flow
                # send a packet
                pass

class Router:
    def __init__(self,env):
        self.queue = []
        self.links = []

    def put(self, packet):
        # Receive a packet
        return

    def receiveAndProcess():
        # Not sure if this is needed
        while True:
            pass

    def send():
        while True:
            # If there are packets to send, send them
            pass



def addFlow(flow):
    # Adds flow to the source host of the flow
    pass


def makePacket():
    return

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
