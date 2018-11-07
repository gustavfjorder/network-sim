ack_size = 64

class Packet:
    def __init__(self,source,destination,sequenceNumber,string_type,size,debug=None):
        self.source = source
        self.destination = destination
        self.debug = debug
        self.type = string_type
        self.sequenceNumber = sequenceNumber
        self.size = size

class ACK(Packet):
    def __init__(self,source,destination,sequenceNumber,ackData):
        Packet.__init__(self,source,destination,sequenceNumber,'ACK',ack_size)
        self.ackData = ackData
        #expecting ackData['Tahoe'] and ackData['Reno']
