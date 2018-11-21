from packets import Data
from math import ceil
import simpy, simpy.util

data_size = 1024
ackTimeOut = 10

# env.now() to track RTT time acktime out is double RTT time
# when we start flow send initial packet to determine RTT

class Tahoe:
    """
    #Implementation of Go Back N
    """
    def __init__(self, name, env, source, destination, size):
        self.id = name
        self.env = env
        self.source = source    # A Host object
        self.source.addFlow(self)
        self.destination = destination  # A host id (e.g. "H2")
        self.packets = self.makePackets(size) # expecting a indexable list as implementation
        self.num_packets = len(self.packets)
        self.done = 0
        self.windowSize = 4
        self.ackTimeOut = 30
        self.windowIndex = (0, min(self.windowSize - 1, self.num_packets - 1)) # no zero indexing here
        self.RTT = [-1 for i in range(self.num_packets)]

        # Start running the flow, delayed
        self.action = simpy.util.start_delayed(env, self.run(), 1000)

    def makePackets(self, size):
        """
        For a give size of packets, I will intialize an array of Packet
        classes to send.
        """
        print(size, data_size, type(size), type(data_size))
        size = size * 1024 * 1024  # In bytes
        N = ceil(size / data_size)

        output = []

        for i in range(N):
            output.append(Data(self.source.id, self.destination, i+1))

        return output

    def packetProcess(self, packet):
        """
        Depending on the algorithm, we process ACK packets differently.
        """
        assert packet.type == 'ACK'
        return packet.ackData['Tahoe'] # should be an int


    def setWindow(self, start):
        """
        just a function to deal with indexing since packets are
        1 indexed while arrays are 0 indexed.
        """
        self.windowIndex = (start - 1, min(start - 1 + self.windowSize - 1, self.num_packets - 1))



    # This should be what the host uses to interrupt flow sortaa
    def ack(self, ackPacket):
        self.put(ackPacket)
        self.action.interrupt()

    # This should be what the host uses to interrupt flow sortaa
    def ack(self, ackPacket):
        self.put(ackPacket)
        self.action.interrupt()

    def put(self, packet):

        nextExpectedPacketNumber = self.packetProcess(packet)
        print(nextExpectedPacketNumber)

        if nextExpectedPacketNumber > self.num_packets:
            """
            If my ACK packet is larger than the number of packets I
            was sending, I am done.
            """
            self.done = 1
        else:
            self.setWindow(nextExpectedPacketNumber)

    def send(self):
        """
        Send all packets in the window.
        """
        start, end = self.windowIndex[0], self.windowIndex[1]
        for i in range(start, end + 1):
            self.source.send(self.packets[i])

    def timeOut(self, time):
        """
        Time passing function
        """
        yield self.env.timeout(time)

    def run(self):
        while not self.done:
            self.send()
            try:
                yield self.env.process(self.timeOut(self.ackTimeOut))

            except simpy.Interrupt: # receive ACK
                pass
                # print('Got an acknowledgement :)')
        print('Done')

class Reno:
    """
    #Implementation of Go Back N
    """
    def __init__(self, name, env, source, destination, size):
        self.id = name
        self.env = env
        self.source = source    # A Host object
        self.source.addFlow(self)
        self.destination = destination  # A host id (e.g. "H2")
        self.packets = self.makePackets(size) # expecting a indexable list as implementation
        self.num_packets = len(self.packets)
        self.done = 0
        self.windowSize = 4
        self.ackTimeOut = 30
        self.windowIndex = (0, min(self.windowSize - 1, self.num_packets - 1)) # no zero indexing here
        self.RTT = [-1 for i in range(self.num_packets)]

        # Start running the flow, delayed
        self.action = simpy.util.start_delayed(env, self.run(), 1000)

    def makePackets(self, size):
        """
        For a give size of packets, I will intialize an array of Packet
        classes to send.
        """
        print(size, data_size, type(size), type(data_size))
        size = size * 1024 * 1024  # In bytes
        N = ceil(size / data_size)

        output = []

        for i in range(N):
            output.append(Data(self.source.id, self.destination, i+1))

        return output

    def packetProcess(self, packet):
        """
        Depending on the algorithm, we process ACK packets differently.
        """
        assert packet.type == 'ACK'
        return packet.ackData['Tahoe'] # should be an int


    def setWindow(self, start):
        """
        just a function to deal with indexing since packets are
        1 indexed while arrays are 0 indexed.
        """
        self.windowIndex = (start - 1, min(start - 1 + self.windowSize - 1, self.num_packets - 1))



    # This should be what the host uses to interrupt flow sortaa
    def ack(self, ackPacket):
        self.put(ackPacket)
        self.action.interrupt()

    # This should be what the host uses to interrupt flow sortaa
    def ack(self, ackPacket):
        self.put(ackPacket)
        self.action.interrupt()

    def put(self, packet):

        nextExpectedPacketNumber = self.packetProcess(packet)
        print(nextExpectedPacketNumber)

        if nextExpectedPacketNumber > self.num_packets:
            """
            If my ACK packet is larger than the number of packets I
            was sending, I am done.
            """
            self.done = 1
        else:
            self.setWindow(nextExpectedPacketNumber)

    def send(self):
        """
        Send all packets in the window.
        """
        start, end = self.windowIndex[0], self.windowIndex[1]
        for i in range(start, end + 1):
            self.source.send(self.packets[i])

    def timeOut(self, time):
        """
        Time passing function
        """
        yield self.env.timeout(time)

    def run(self):
        while not self.done:
            self.send()
            try:
                yield self.env.process(self.timeOut(self.ackTimeOut))

            except simpy.Interrupt: # receive ACK
                pass
                # print('Got an acknowledgement :)')
        print('Done')

