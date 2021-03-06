# For link buffer
import collections
import simpy.util

class Link:
    '''
    Link class.
    To send things through a link, yield to Link.put(packet) (as a simpy process).
    Link.run is a simpy process that will constantly run.
    '''

    def __init__(self, env, id, delay, bufferSize, rate, source, destination, \
                 debug):
        ''' Initializes link '''

        # Passed in attributes
        self.id = id
        self.env = env
        self.rate = rate               # Mbps
        self.propagationDelay = delay  # ms
        self.bufferSize = bufferSize   # bytes
        self.debug = debug             # Whether or not to print

        # Objects representing source/dest
        self.source = source                  # a host or router
        self.destination = destination        # a host or router

        # Run (add to env)
        self.action = env.process(self.run())

        # An infinite size queue. We internally enforce buffer limits.
        self.buffer = collections.deque()
        self.bufferUsed = 0;           # bytes

        # For monitoring
        self.bitsSent = 0
        self.packetsDropped = 0

        # Start running link
        self.action = self.env.process(self.run())

    def transmissionDelay(self, packet):
        # 8 for byte to bit
        # 10^6 for Mbps to bps
        return packet.size * 8 / (self.rate * 10**6)

    def put(self, packet):
        '''
        Receives a packet.

        Put the packet in the buffer. Then wait the transmissionTime for the
        packet to finish.

        Warning: This should not get called by two things, because the
        transmission delays will get messed up, probably.
        Warning: This is a generator, not a function so must be called as such
        or created as a simpy process.

        The generator for Link will deal with the link's side of transmission
        delay and propagation delay.

        Put into the buffer (run deals with transmission delay, so do this
        first) if buffer not full. Otherwise, drop the packet.
        '''

        if self.bufferUsed + packet.size <= self.bufferSize:
            if self.debug:
                print(self.id, "in buffer: ", packet, self.env.now)
            self.buffer.append(packet)
            self.bufferUsed += packet.size
        else: # Drop the packet
            if self.debug:
                print(self.id, " dropped, ", packet)
            self.packetsDropped += 1

        # Wait transmissionTime of the packet, to hold back source.
        # 8 for byte to bit
        # yield self.env.timeout(self.transmissionDelay(packet)) # Not sure if yield is right


    def finishSendingPacket(self, packet):
        self.destination.put(packet)
        yield self.env.timeout(0)

    def run(self):
        '''
        Sends packets down the link. Runs continuously as a simpy process.

        Warning: This is a generator, not a function so must be called as such
        or created as a simpy process.
        Warning: relies on host or router 'put' is a generator, not a function
        '''
        while True:
            # If buffer not empty, send all the packets in buffer.
            # After propagation delay (plus transmission), they will arrive.
            # Space departures by transmission delay.

            while self.buffer:

                # Get packet (popleft is FIFO)
                packet = self.buffer.popleft()

                if self.debug:
                    print(self.id, "transmitting", packet, "to", self.destination.id)

                # Wait transmission delay
                yield self.env.timeout(self.transmissionDelay(packet))
                # The packet has been sent, so buffer has been freed
                self.bufferUsed -= packet.size

                # Monitoring
                self.bitsSent += packet.size

                if self.debug:
                    print(self.id, "sending", packet, "to", self.destination.id)

                # Pass to router after propagationDelay time (but don't
                # wait).
                # start_delayed is like process, but will start the process
                # after a time delay.
                simpy.util.start_delayed(self.env, \
                                     self.finishSendingPacket(packet), \
                                     self.propagationDelay)
            # Check again after 0.1 ms.
            yield self.env.timeout(0.1)
