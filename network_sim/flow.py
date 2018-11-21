from packets import Packet
from math import ceil
import simpy
import math
from collections import defaultdict

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

        # Start running the thing
        self.timeOutFlag = env.event()
        self.action = env.process(self.run())

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
            output.append(Packet(self.source.id, self.destination, i+1, 'Data', data_size))

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

    def put(self, packet):
        print("Enter put method:",packet.sequenceNumber)
        nextExpectedPacketNumber = self.packetProcess(packet)
        print("Finished packet process:",packet.sequenceNumber)


        print(nextExpectedPacketNumber)

        if nextExpectedPacketNumber > self.num_packets:
            """
            If my ACK packet is larger than the number of packets I
            was sending, I am done.
            """
            self.done = 1
        else:
            self.setWindow(nextExpectedPacketNumber)

    def send(self, source):
        """
        Send all packets in the window.
        """
        start, end = self.windowIndex[0], self.windowIndex[1]
        for i in range(start, end + 1):
            source.send(self.packets[i])

    def timeOut(self, time):
        """
        Time passing function
        """
        yield self.env.timeout(time)

    def run(self):
        while not self.done:
            self.send(self.source)
            try:
                yield self.env.process(self.timeOut(self.ackTimeOut))

            except simpy.Interrupt: # receive ACK
                pass
                # print('Got an acknowledgement :)')
        print('Done')

class TCPPhase:
    def __init__(self):
        self.phase = "Slow Start"
        self.threshold = None

    def setSlow(self):
        assert self.phase == "CA"
        self.phase = "Slow Start"
        self.threshold = None #yes?

    def setFast(self):
        assert self.phase == "Slow Start"
        self.phase = "CA"

class Reno:
    """
    # TODO:
    implement timeout properly
    slow start / congestion avoidance

    """
    def __init__(self, name, env, source, destination, size):

        """variables set by arguments"""
        self.id = name
        self.env = env
        self.source = source    # A Host object
        self.source.addFlow(self)
        self.destination = destination  # A host id (e.g. "H2")
        self.packets = self.makePackets(size) # expecting a indexable list as implementation
        self.num_packets = len(self.packets)
        self.done = 0

        """variables not set by arguments"""
        self.dup_dict = {}

        self.windowSize = 1 #default as described by slow start
        self.ackTimeOut = 20 #where did we get this from?
        self.windowIndex = (0, min(self.windowSize - 1, self.num_packets - 1)) #min ensures that our indexes are not larger than the lst length
        self.RTT = [-1 for i in range(self.num_packets)]
        self.unacknowledged_packets = set()

        self.phase = TCPPhase()

        # Start running flow
        self.action = env.process(self.run())

    def masterUpdate(self):
        if self.phase.phase == "Slow Start":
            self.slowUpdate()
        elif self.phase.phase == "CA":
            self.caUpdate()

    def slowUpdate(self):
        assert self.phase.phase == "Slow Start"

        if self.phase.threshold and self.phase.threshold <= self.windowSize:
            self.phase = "CA"

        else:
            self.windowSize += 1

    def caUpdate(self):
        assert self.phase.phase == "CA"
        #assertion statement about threshold
        self.windowSize += max(1,floor(1/self.windowSize))

    def makePackets(self, size):
        """
        For a give size of packets, I will intialize an array of Packet
        classes to send.
        """
        size = size * 1024 * 1024  # In bytes
        N = ceil(size / data_size)

        packets = []

        for i in range(N):
            packets.append(Packet(self.source.id, self.destination, i+1, 'Data', data_size))
        return packets

    def packetProcess(self, packet):
        """
        Depending on the algorithm, we process ACK packets differently.
        """
        assert packet.type == 'ACK'
        return packet.ackData['Reno']


    def setWindow(self, start):
        """
        just a function to deal with indexing since packets are
        1 indexed while arrays are 0 indexed.
        """
        self.windowIndex = (math.floor(start - 1),math.floor( min(start - 1 + self.windowSize - 1, self.num_packets - 1)))

    def ack(self, ackPacket):
        """
        Handle ack from hsot
        """
        print('hello')
        print("Flow",self.id,"in ack method",ackPacket.ackData["Reno"])
        self.put(ackPacket)
        self.action.interrupt()

        try:
            yield self.env.process(self.timeOut(self.ackTimeOut))
            self.timeOutFlag.succeed()
        except simpy.Interrupt:
            pass

    def put(self, packet):
        nextExpectedPacketNumber = self.packetProcess(packet)

        print(self.id,"expected:",min(self.unacknowledged_packets[0])+1)
        print(self.id,"got     :",nextExpectedPacketNumber)
        if nextExpectedPacketNumber == min(self.unacknowledged_packets)+1:
            # print("deleting unack'ed packet",self.unacknowledged_packets[0])
            self.masterUpdate()
            self.unacknowledged_packets.remove(nextExpectedPacketNumber-1)

        elif nextExpectedPacketNumber > self.num_packets:
            print("DONE")
            self.done = 1
        else:
            if nextExpectedPacketNumber-1 not in dup_dict:
                self.dup_dict[nextExpectedPacketNumber-1] = 1
            else:
                self.dup_dict[nextExpectedPacketNumber-1] +=1
                self.windowSize = self.windowSize/2

        self.setWindow(nextExpectedPacketNumber)
        #yield with a timeout

    def send(self, source):

        start, end = self.windowIndex[0], self.windowIndex[1]
        for i in range(start, end + 1):
            source.send(self.packets[i])
            assert self.packets[i].sequenceNumber not in self.unacknowledged_packets
            self.unacknowledged_packets.add(self.packets[i].sequenceNumber)


    def timeOut(self, time):
        """
        Time passing function
        """
        yield self.env.timeout(time)

    def sendLoop(self):
        while not self.done:
            if len(self.unacknowledged_packets) <= self.windowSize:
                self.send(self.source)


    def run(self):
        """Everything till the while loop is just for the first packet sent"""
        self.send(self.source)

        try:
            yield self.env.process(self.timeOut(self.ackTimeOut))
            self.run()

        except simpy.Interrupt:

            self.sendAction = env.process(self.sendLoop())

            while not self.done:
                yield self.timeOutFlag #if timeout succeeds we continue
                print("Timeout bitch")
                self.windowSize = 1
                self.setWindow(min(self.unacknowledged_packets))



"""
        while not self.done:
            if len(self.unacknowledged_packets) == 0:
                self.send(self.source)
            try:
               yield self.env.process(self.timeOut(self.ackTimeOut))
            except simpy.Interrupt:
                print("interrupted")
                pass
        print('Done')
"""
