from packets import ACK
from nodeParent import nodeParent

class Host(nodeParent):
    # inherits from nodeParent
    def __init__(self,env, name, links):
        super(Host, self).__init__(env, name, links)
        self.link = self.links # hosts only have one link
        self.flow = None
        self.type = "host"

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
        # Pass it to flow
        # receive ack OR send ack if it isn't an ack
        # Ignore routing packets
        if(packet.type == 'ACK'):
            ack(self.env, self.flow, packet)
        elif( packet.type == 'data'):
            # If Packet is not an Acknowledgement, need to  send an acknowledgement
            # new destination is the source, get this from the flow\
            ackData = None  # initalize this later
            ackPacket = ACK(packet.destination, packet.source, \
                packet.sequenceNumber, ackData )
            self.flow.put(ackPacket)


    def run(self):
        while (True):
            # if there is a flow
            if(self.flow):
                # send a packet
                self.flow.send(self)

    # This should be what the host uses to interrupt flow sortaa
    def ack(flow, ackPacket):
        flow.put(ackPacket)
        flow.action.interrupt()




# host should call recieve in Flow
