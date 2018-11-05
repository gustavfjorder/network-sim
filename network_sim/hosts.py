import flow, acknowledgedPackets

class Host:
    def __init__(self,env,name, link):
        self.env = env
        self.id = name
        addLink(link)
        self.flows = []

    def addFlow(flow):
        self.flows.append(flow)

    def addLink(link):
        self.link = link

    #def addPort(self):
        #return

    def send(self, packet):
        # being called by Flow ???
        # From flow to link
        self.link.put(packet)
        return

    def put(self, packet):
        # Receive a packet from link
        # Pass it to flow
        self.flows
        # receive ack OR send ack if it isn't an ack
        if(packet.type == 'ACK'):
            pass
        else:
            # Packet is not an Acknoledgement, need to  send an acknowledgement
            # new destination is the source, get this from the flow
            awkPacket = Packet(self.env, packet.)
        pass

    def run(self):
        while (True):
            # if there is a flo
                # send a packet
                pass

# host should call recieve in Flow
