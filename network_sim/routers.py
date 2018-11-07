import flow, packets

class Routers:
    def __init__(self,env, name, links):
        self.env = env
        self.id = name
        self.links = links
        self.flows = None # TODO
        self.routingTable = None # TODO


    def addFlow(sekf,flow):
        self.flows.append(self, flow)

    def send(self, packet):
        # being called by Flow ???
        # From flow to link
        link = None # TODO
        link.put(packet)
        return

    def findFlowForPackage(self, package):
        for flow in self.flows:
            if(flow.id == package.flowId):
                return flow

    def put(self, packet):
        # Receive a packet from link
        # Pass it to flow
        flow = self.findFlowForPackage()



    def run(self):
        while (True):
            # if there is a flow
            if(self.flow):
                # send a packet
                self.flow.send(self)



# host should call recieve in Flow
