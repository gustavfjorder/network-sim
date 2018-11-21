from packets import Routing
from nodeParent import nodeParent
from copy import copy
from math import inf

class Router(nodeParent):
    #inherits from nodeParent
    def __init__(self, env, name, links):
        super(Router, self).__init__(env, name, links)
        self.type = 'router'

        # Form "some node": link, where link is the next link to pass to
        # We will need a way to correlate nodes with links.
        self.routingTable = {}

        ## For dynamic routing

        # For during construction of routing table
        # Elements in the allCostsTable are in the form (from, to, cost)
        self.allCostsTable = []
        # List of the most recent routing packet received {source: timestamp}
        self.recentRoutingPackets = {}
        # Let the routing tables update periodically
        self.env.process(self.run_routingInfo())
        # Routing refresh period
        self.refreshRoutingTime = 5000   # 5 sec, which is what the test cases do


    def send(self, packet):
        dest = packet.destination
        nextLink = self.routingTable[dest]
        # look up link to send to in routing Table
        nextLink.put(packet)
        return

    def put(self, packet):
        # Receive a packet from a link
        print(self.id, "receive", packet)
        if (packet.type == "routing"):
            self.addRoutingTableInfo(packet)
        else:
            self.send(packet)

    ### Dynamic routing functions
    # TODO: addToAllCosts. Better way of preventing infinite loop packets
    def addRoutingTableInfo(self, packet):
        '''
        Receive a packet with routing table info.
        Called every time a routing packet is received.
        '''

        # Helper function
        def addToAllCosts(data):
            '''
            Takes data in the form (from, {to: cost}), and adds this info to
            self.allCostsTable.
            '''

            # Remove old cost data for the source of this packet
            self.allCostsTable = [i for i in self.allCostsTable if i[0] != data[0]]

            # Add new cost data
            for to, cost in data[1].items():
                self.allCostsTable.append((data[0], to, cost))

        pckt_source = packet.data[0]

        # If we haven't received a routing packet from this source,
        # add it to our recentRoutingPackets dictionary.
        if pckt_source not in self.recentRoutingPackets:
            self.recentRoutingPackets[pckt_source] = packet.timeSent - 1

        # If this packet was generated after the one we know of,
        # update our knowledge.
        if self.recentRoutingPackets[pckt_source] < packet.timeSent:

            # Update info about the most recent routing packet from this
            # packet's source.
            self.recentRoutingPackets[pckt_source] = packet.timeSent

            # Add the packet to the all costs table and update lists of nodes that
            # exist in the network and nodes that we have costs from.
            addToAllCosts(packet.data)

            # Re-run Dijkstra. TODO: Only when something changes?
            self.createRoutingTable()

            # Pass on the info to all other nodes connected
            for link in self.links:
                link.put(packet)


    def createRoutingTable(self):
        '''
        Constructs a shortest path using Dijsktra.
        Called when we have all knowledge of the graph to construct a
        shortest path.
        Warning: This will only work for connected networks.
        '''

        # Helper function
        def linkFromNode(node):
            '''
            Returns a connected link object that has node at the other side
            or None if the node isn't connected directly.
            '''
            return next((link for link in self.links if link.destination.id == node), None)


        # All nodes we could theoretically get to.
        allNodes = set([dest for source, dest, cost in self.allCostsTable])

        # Format {final destination: (cost, prev)}
        minCostsSoFar = {node: (inf, None) for node in allNodes}
        # A dictionary of {dest: prev}
        reachableNodes = {}

        # Add self to reachable nodes
        minCostsSoFar[self.id] = (0, self.id)
        # Run Dijkstra
        while minCostsSoFar != {}:
            # Find the smallest-cost reachable node, to update graph with
            nextFixed, (fixedCost, fixedPrev) = \
                     min(minCostsSoFar.items(), key = lambda item: item[1][0])
            # Fix this node's path
            reachableNodes[nextFixed] = fixedPrev
            # Remove this node from unfound nodes
            del minCostsSoFar[nextFixed]

            for source, to, cost in [i for i in self.allCostsTable if i[0] == nextFixed]:
                # If the to is still unsettled and the cost using nextFixed is
                # smaller than the current cost,
                if to in minCostsSoFar \
                   and fixedCost + cost < minCostsSoFar[to][0]:
                    minCostsSoFar[to] = (fixedCost + cost, nextFixed)

        print(self.id, "allCostsTable: ", self.allCostsTable)
        print(self.id, "dijkstra: ", reachableNodes)


        # Ran Dijskra, now extract information by running down the 'previous'
        # path of reachableNodes and change to the link info
        routingTable = {}
        for dest, prev in reachableNodes.items():
            prevPrev = dest
            nextPrev = prev
            print(self.id, dest, prevPrev, nextPrev)
            while nextPrev != self.id:
                prevPrev = nextPrev
                nextPrev = reachableNodes[prevPrev]
            print(self.id, dest, prevPrev, nextPrev)
            routingTable[dest] = linkFromNode(prevPrev)


        print(self.id, "routing table: ", routingTable)
        # Start using the new routing table.
        self.routingTable = routingTable

    def run_routingInfo(self):
        '''
        Inititalizes another round of routing every refreshRoutingTime, which will
        trigger a refresh for all connected routers.
        Only one router in the network needs to run this, though all will run it.
        '''
        while True:
            # Initialize a new routing cycle, if another router hasn't already
            if not self.allCostsTable:
                self.sendMyInfo()

            # Wait some time
            yield self.env.timeout(self.refreshRoutingTime)

    # Helper functions for dynamic routing

    def sendMyInfo(self):
        '''
        Sends data to connected routers about local link costs and connected
        hosts/routers.
        Data is of form (from, {to: (cost, isHost)}), where from is self.id.
        '''

        # Refresh the router's costs
        # A dictionary of {nodeID: cost}
        # Could be more efficient
        costs = {}
        for link in self.links:
            cost = 5 * link.bufferUsed / link.bufferSize + link.propagationDelay
            costs[link.destination.id] = cost

        # Data is of form (from, {to: cost}),
        # where from is self.id.
        data = (self.id, copy(costs))
        packet = Routing(self.id, data, self.env.now)

        # Pretend like we just received this packet to update routing table.
        # This will "forward" the packet
        self.addRoutingTableInfo(packet)
