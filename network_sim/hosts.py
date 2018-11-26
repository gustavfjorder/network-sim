from packets import ACK

class Host:
    def __init__(self,env, name, link, debug):
        self.env = env
        self.id = name
        self.link = link
        self.flow = None

        # Whether or not to output what's happening
        self.debug = debug

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
        if self.debug:
            print(self.id, "receive ", packet)
        # If it's an acknowledgement, pass it to flow
        # Otherwise, send ack for the packet
        if packet.type == 'ACK':
            self.flow.ack(packet)
        elif packet.type=='data':
            print('ifyay')
            # Packet is not an Acknowledgement, need to  send an acknowledgement
            # new destination is the source, get this from the flow

            # Update most recent packet received
            if packet.source not in self.lastPacketReceived:
                self.lastPacketReceived[packet.source] = packet.sequenceNumber
            else:
                if self.lastPacketReceived[packet.source] + 1 == packet.sequenceNumber:
                    self.lastPacketReceived[packet.source] = packet.sequenceNumber

            ackData = self.lastPacketReceived[packet.source] + 1
<<<<<<< HEAD
            print("barrier1")
=======
>>>>>>> refs/remotes/origin/master
            ackPacket = ACK(packet.destination, packet.source, \
                packet.sequenceNumber, ackData )
            print("barrier2")
            self.link.put(ackPacket)


    def run(self):
        while (True):
            # if there is a flow
            if(self.flow):
                # send a packet
                self.flow.send(self)




# host should call recieve in Flow
