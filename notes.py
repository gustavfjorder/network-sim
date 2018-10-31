AWKNOWLEDGEMENT_PACKET_SIZE = 64
# may assume that acknowledgement packets have a fixed size of 64 bytes.
FLOW_GENERATED_PACKET_SIZE = 1024
# may assume that flow-generated data packets have a fixed size of 1024 bytes,
# including any packet headers or trailers

class Host:
    def __init__(self,env,name,port):
        self.link = None
        self.flows = []

    #def addPort(self):
        #return

    def send(self, packet):
        # From flow to link
        return

    def receive(self, packet):
        # From link to flow
        # receive ack OR send ack if it isn't an ack
        pass

    def run(self):
        while (True):
            # if there is a flow

                # send a packet
                pass

class Router(algorith?):
    def __init__(self,env):
        self.queue = []
        self.links = []

    def receivePacket(packet):
        return

    def sendPacket(packet):
        return

    def receiveAndProcess():
        # Not sure if this is needed
        while True:
            pass

    def send():
        while True:
            # If there are packets to send, send them
            pass

class Packet:
    def __init__(self,env,destination,information):
        self.destination = destination
        self.information = information
        self.size = len(information)

class Link: #use shared resource for the link?
    def __init__(self, env, delay, bufferSize, rate):
        self.rate = rate  # Mbps
        self.buffer = []
        self.propagationDelay = delay  # ms
        self.bufferSize = bufferSize
        self.source = None
        self.destination = None

    def receivePacket(packet):
        # wait the amount of time it would take to transmit the packet
        # add the packet to the Link. Then after delay time, pass to the next
        # router. May need multiple functions. And deal with both directions of
        # link.
        self.enqueue()
        pass

    def enqueue(self, packet):
        # adds packet to buffer
        pass

    def run(self):
        while True:
            if #buffer not empty
                #send a packet
                propagate
            pass

    def propagate(self, packet):
        # first wait transmission delay (packet size / rate)
        # then make an event that after propagation delay, passes the packet to
        # the destination. However, doesn't just wait and hold up other
        # packets
        # Finally, waits the transmission delay to arrive at the destination.
        # OR put in a waiting area
        transmissionDelay = packet.size / self.rate


        #need to simpy this
class Flow:
    def __init__(self,source,destination,size,start):
        self.size = size
        self.sizeLeft = size
        self.source = source
        self.destination = destination
        self.unacknolwedgedPackets = []
        # or self.acknowledgedPackets?
    def run(self,start):
        while True:

            yield

    def receive(self, packet):
        # Receive an acknow

def addFlow(flow):
    # Adds flow to the source host of the flow



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
