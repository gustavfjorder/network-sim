import flow, packets

class Host:
    def __init__(self,env,name, link):
        self.env = env
        self.id = name
        addLink(link)
        self.flow = None

    def addFlow(flow):
        self.flow = flow

    def addLink(link):
        self.link = link

    def send(self, packet):
        # being called by Flow ???
        # From flow to link
        self.link.put(packet)
        return

    def put(self, packet):
        # Receive a packet from link
        # Pass it to flow
        self.flow.packetProcess(packet)
        # receive ack OR send ack if it isn't an ack
        if(packet.type == 'ACK'):
            # Remove packet from flow.packets
            pass
        else:
            # Packet is not an Acknoledgement, need to  send an acknowledgement
            # new destination is the source, get this from the flow\
            ackData = None  # initalize this later
            ackPacket = Packet(self.env, packet.destination, packet.source, \
                packet.sequenceNumber, ackData )
            self.send(ackPacket)

    def run(self):
        while (True):
            # if there is a flow
            if( self.flow):
                # send a packet
                self.send(packet);

# host should call recieve in Flow
