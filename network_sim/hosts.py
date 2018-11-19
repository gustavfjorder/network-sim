from packets import Packet, nodeParent

class Host(nodeParent):
    # inherits from nodeParent
    def __init__(self,env, name, links):
        super.__init__()
        self.env = env
        self.id = name
        self.link = self.links[0] # hosts only have one link
        self.flow = None
        sekf.type = "host"

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
        super.put(self, packet)
        # Receive a packet from link
        # Pass it to flow
        # receive ack OR send ack if it isn't an ack
        if(packet.type == 'ACK'):
            ack(self.env, self.flow, packet)
        else:
            # Packet is not an Acknowledgement, need to  send an acknowledgement
            # new destination is the source, get this from the flow\
            ackData = None  # initalize this later
            ackPacket = Packet(self, packet.destination, packet.source, \
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
