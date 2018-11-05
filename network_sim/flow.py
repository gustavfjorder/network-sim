from packets import Packet

data_size = 1024

class Tahoe:
    """
    #Implementation of Go Back N
    """
    def __init__(self,env,source,destination,size,windowSize,ackTimeOut):
        self.env = env
        self.source = source
        self.destination = destination
        self.packets = self.makePackets(size) #expecting a indexable list as implementation
        self.num_packets = len(self.packets)
        self.done = 0
        self.windowSize = windowSize
        self.ackTimeOut = ackTimeOut
        self.windowIndex = (0, min(self.windowSize - 1, self.num_packets - 1)) #no zero indexing here

    def makePackets(size):
        size = size * 1024 * 1024# In bytes
        N = size / data_size

        output = []
        
        for i in range(N):
            output.append(Packet(self.source,self.destination,i+1, 'Data', data_size))

        return output

    def packetProcess(packet):
        assert packet.type == 'ACK'
        return packet.ackData['Tahoe'] # should be an int


    def setWindow(start):
        self.windowIndex = (start - 1, min(nextExpectedPacketNumber - 1 + self.windowSize - 1, self.num_packets - 1))

    def put(self, packet): #receiving
        nextExpectedPacketNumber = self.packetProcess(packet)
        
        if nextExpectedPacketNumber > self.num_packets:
            self.done = 1
        else:
            setWindow(nextExpectedPacketNumber)

    def send(self,source):
        start, end = self.windowIndex[0], self.windowIndex[1]
        for i in range(start, end + 1):
            source.put(self.packets[i])

    def timeOut(self,time):
        yield self.env.timeout(time)

    def run(self):
        while not self.done:
            self.put()
            try:
                yield self.env.process(self.env.timeout(self.ackTimeOut))

            except simpy.Interrupt: #receive ACK
                pass
                #print('Got an acknowledgement :)')

# This should be what the host uses to interrupt me sortaa
def ack(env, flow):
    car.put(ackPacket)
    car.action.interrupt()