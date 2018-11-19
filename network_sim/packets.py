ack_size = 64
data_size = 1024
routing_size = 64  # TODO: Actual number

class Packet:
    def __init__(self,source,destination,string_type,size,debug=None):
        self.source = source
        self.destination = destination
        self.debug = debug
        self.type = string_type
        self.size = size

class Data:
    def __init__(self,source,destination,sequenceNumber):
        Packet.__init__(self,source,destination,'data',data_size)
        self.sequenceNumber = sequenceNumber


class ACK(Packet):
    def __init__(self,source,destination,sequenceNumber,ackData):
        Packet.__init__(self,source,destination,'ACK',ack_size)
        self.sequenceNumber = sequenceNumber
        self.ackData = ackData
        #expecting ackData['Tahoe'] and ackData['Reno']

class Routing(Packet):
    def __init(self, source, data):
        # TODO: None destination
        Packet.__init__(self, source, None, 'routing', routing_size)
        self.data = data
