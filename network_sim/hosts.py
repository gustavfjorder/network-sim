from packets import ACK

class Host:
    def __init__(self,env, name, link):
        self.env = env
        self.id = name
        self.link = link
        self.flow = None

        # Dictionary because host could receive multiple flows
        self.lastPacketReceived = {}

    def addFlow(self, flow):
        '''
        Flow calls this when it initializes
        '''
        self.flow = flow

    def send(self, packet):
        # being called by Flow ???
        # From flow to link
        self.link.put(packet)
        return

    def put(self, packet):
        # Receive a packet from link

        # If it's an acknowledgement, pass it to flow
        # Otherwise, send ack for the packet
        if(packet.type == 'ACK'):
            self.flow.ack(packet)
        else:
            # Packet is not an Acknowledgement, need to  send an acknowledgement
            # new destination is the source, get this from the flow

            # Update most recent packet received
            if packet.source not in self.lastPacketReceived:
                self.lastPacketReceived[packet.source] = packet.sequenceNumber
            else:
                if self.lastPacketReceived[packet.source] + 1 == packet.sequenceNumber:
                    self.lastPacketReceived[packet.source] = packet.sequenceNumber

            ackData = {"Tahoe": self.lastPacketReceived[packet.source] + 1}
            ackPacket = ACK(packet.destination, packet.source, \
                packet.sequenceNumber, ackData )
            self.link.put(ackPacket)


    def run(self):
        while (True):
            # if there is a flow
            if(self.flow):
                # send a packet
                self.flow.send(self)




# host should call recieve in Flow
