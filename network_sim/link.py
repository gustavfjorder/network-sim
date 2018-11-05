import collections

class Link:
    def __init__(self, env, id, delay, bufferSize, rate):
        self.id = id
        self.env = env
        self.rate = rate               # Mbps
        # An infinite size queue. We internally enforce limits.
        self.buffer = collections.deque()
        self.propagationDelay = delay  # ms
        self.bufferSize = bufferSize   # bytes
        self.bufferUsed = 0;           # bytes
        self.source = None             # a host or router
        self.destination = None        # a host or router

        # For monitoring
        self.bitsSent = 0
        self.packetsDropped = 0

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
            self.buffer.append(packet)
            self.bufferUsed += packet.size
        else: # Drop the packet
            self.packetsDropped += 1

        # Wait transmissionTime of the packet, to hold back source.
        transmissionDelay = packet.size * 8 / self.rate   # 8 for byte to bit
        yield self.env.timeout(transmissionDelay) # Not sure if yield is right

    # This is a generator, not a function so must be called as such
    # or created as a simpy process.
    # Warning: relies on host or router 'put' is a generator, not a function
    def run(self):
        while True:
            # If buffer not empty, send all the packets in buffer.
            # After propagation delay (plus transmission), they will arrive.
            # Space departures by transmission delay.
            while self.buffer:
                # Get packet (popleft is FIFO)
                packet = self.buffer.popleft()

                # Wait transmission delay
                # 8 for byte to bit
                transmissionDelay = packet.size * 8 / self.rate
                yield self.env.timeout(transmissionDelay)
                # The packet has been sent, so buffer has been freed
                self.bufferUsed -= packet.size

                # Monitoring
                self.bitsSent += packet.size

                # Pass to router after propagationDelay time (but don't
                # wait).
                # start_delayed is like process, but will start the process
                # after a time delay.
                simpy.util.start_delayed(self.env, \
                                     self.destination.put(packet), \
                                     self.propagationDelay)
            # Check again after 0.1 ms.
            yield self.env.timeout(0.1)
