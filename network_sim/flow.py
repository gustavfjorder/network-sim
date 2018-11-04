"""
Flow(Tahoe):
    def __init__(self,env,source,destination,size):
        self.size = size #for now size is in packets
        self.source = source
        #self.destination = destination #useless variable for now



    def run(self,start=1.0):
        while True:

            yield

    def receive(self, packet):
        value = self.packetProcess(packet)

        # Receive an acknow

    def windowControl

#class Algorithm:

#class Reno(Tahoe):

class Tahoe:
    """
    #Implementation of Go Back N
    """
    def __init__(self,windowSize,ackTimeOut):
        self.windowSize = windowSize
        self.ackTimeOut = ackTimeOut
        self.windowIndex = (0, self.windowSize - 1) #no zero indexing here
        self.send = 

    def receive(self, nextExpectedPacketNumber):
        self.windowIndex = (nextExpectedPacketNumber - 1, nextExpectedPacketNumber - 1 + self.windowSize - 1)
        # set windowIndex based on packetnumber

    def failed(self):
        #send all packets in window

"""
class Tahoe:
    """
    #Implementation of Go Back N
    """
    def __init__(self,env,source,destination,size,windowSize,ackTimeOut):
        self.env = env
        self.source = source
        self.destination = destination
        self.packets = [i for i in range(1,size + 1)]
        self.done = 0
        self.windowSize = windowSize
        self.ackTimeOut = ackTimeOut
        self.windowIndex = (0, self.windowSize - 1) #no zero indexing here

    def receive(self, packet):
        nextExpectedPacketNumber = packetProcess(packet)
        self.windowIndex = (nextExpectedPacketNumber - 1, nextExpectedPacketNumber - 1 + self.windowSize - 1)
        # set windowIndex based on packetnumber

    def put(self):
        start, end = self.windowIndex[0], self.windowIndex[1]
        for i in range(start, end + 1):
            #add thing into queue???
        #send all packets in window

    def run(self):
        while not self.done:
            self.put()
            if receive: # interrupt
                self.receive(packet)
            yield??
            else:
                self.retransmit
