AWKNOWLEDGEMENT_PACKET_SIZE = 64
# may assume that acknowledgement packets have a fixed size of 64 bytes.
FLOW_GENERATED_PACKET_SIZE = 1024
# may assume that flow-generated data packets have a fixed size of 1024 bytes,
# including any packet headers or trailers

# For Link
import queue

# By default, if a function has a yield statement in it, it is a generator.

# Note: For acknowledgements, we should be saying I'm expecting this packet next
# instead of saying I just received this packet
# packet 1 received. ACK: expecting packet 2 next.
# Sorry, above is only true for Tahoe, and different for Reno
# need to discuss this. Look at page 92 of WP
class Host:
    def __init__(self,env,name,port):
        self.link = None
        self.flows = []

    #def addPort(self):
        #return

    def send(self, packet):
        # From flow to link
        return

    def put(self, packet):
        # Receive a packet from link
        # Pass it to flow
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

class Packet:
    def __init__(self,env,destination,information):
        self.destination = destination
        self.information = information
        self.size = len(information)   # bits? bytes?

        # something that the lecture notes say each packet has in the header
        # to discuss
        self.sequenceNumber = None
        self.ackNumber = None

class Link:
    def __init__(self, env, delay, bufferSize, rate):
        self.env = env
        self.rate = rate  # Mbps
        # An infinite size queue. We internally enforce limits.
        self.buffer = queue.Queue()    #
        self.propagationDelay = delay  # ms
        self.bufferSize = bufferSize   # bit/bytes?
        self.bufferUsed = 0;           # bit/bytes?
        self.source = None             # a host or router
        self.destination = None        # a host or router

    # This is a generator, not a function so must be called as such
    # or created as a simpy process.
    def put(self, packet):
        # Receives a packet.
        #
        # Put the packet in the buffer. Then wait the transmissionTime for the
        # packet to finish.
        #
        # Warning: This should not get called by two things, because the
        # transmission delays will get messed up, probably.
        #
        # The generator for Link will deal with the link's side of transmission
        # delay and propagation delay.

        # Put into the buffer (run deals with transmission delay, so do this
        # first) if buffer not full. Otherwise, drop the packet.
        if self.bufferUsed + packet.size <= self.bufferSize:
            self.buffer.put(packet)
            self.bufferUsed += packet.size
        else:
            pass     # Effectively drop the packet

        # Wait transmissionTime of the packet, to hold back source.
        transmissionDelay = packet.size / self.rate
        yield self.env.timeout(transmissionDelay) # Not sure if yield is right

    # This is a generator, not a function so must be called as such
    # or created as a simpy process.
    # Warning: relies on host or router 'put' is a generator, not a function
    def run(self):
        while True:
            # If buffer not empty, send all the packets in buffer.
            # After propagation delay (plus transmission), they will arrive.
            # Space departures by transmission delay.
            while not self.buffer.empty():
                # Get packet left
                packet = self.buffer.get()

                # Wait transmission delay
                transmissionDelay = packet.size / self.rate
                yield self.env.timeout(transmissionDelay)
                # The packet has been sent, so buffer has been freed
                self.bufferUsed -= packet.size;

                # Pass to router after propagationDelay time (but don't
                # wait).
                # start_delayed is like process, but will start the process
                # after a time delay.
                simpy.util.start_delayed(self.env, \
                                     self.destination.put(packet), \
                                     self.propagationDelay)
            # Check again after 1 ms.
            yield self.env.timeout(1)


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
