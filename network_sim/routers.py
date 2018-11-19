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
        # These are all the routers in the graph that we know exist. Set so no duplicates.
        self.allRouters = set()
        # These are all the nodes that we have received cost info about
        self.knownNodes = set()
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
        if (packet.type == "routing"):
            addRoutingTableInfo(packet)
        else:
            self.send(packet)

    ### Dynamic routing functions

    def addRoutingTableInfo(packet):
        '''
        Receive a packet with routing table info.
        Called every time a routing packet is received.
        '''

        # If we haven't sent our own info, do that, probably
        # TODO: This is not a perfect way to manage this, but fine
        if not self.allCostsTable:
            self.sendMyInfo(self)

        # If we haven't yet received this packet information, use it. Otherwise
        # ignore.
        if packet.data[0] not in self.knownNodes:

            # Add the packet to the all costs table and update lists of nodes that
            # exist in the network and nodes that we have costs from.
            self.addToAllCosts(packet.data)

            # The node we haven't received costs from will be empty when we have
            # a full view of the network
            unknownNodes = self.allRouters - self.knownNodes

            # If we have all the info of all known routers, then run Dijkstra
            # Otherwise, wait until more packets have been received
            if not unknownNodes:
                createRoutingTable(self)

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
        def linkFromNode(self, node):
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
        minCostsSoFar[self.id] = (0, None)

        # Run Dijkstra
        while reachableNodes != allNodes:
            nextFixed = min(minCostsSoFar)
            fixedCost, fixedPrev = minCostsSoFar[nextFixed]
            reachableNodes[nextFixed] = (fixedCost, fixedPrev)
            # Remove this node from unfound
            del minCostsSoFar[nextFixed]

            for source, to, cost in [i for i in self.allCostsTable if i[0] == nextFixed]:
                # If the to is still unsettled and the cost using nextFixed is
                # smaller than the current cost,
                if to in minCostsSoFar \
                   and fixedCost + cost < minCostsSoFar[to][0]:
                    minCostsSoFar[to] = (fixedCost + cost, nextFixed)

        # Ran Dijskra, now extract information by running down the 'previous'
        # path of reachableNodes and change to the link info
        routingTable = {}
        for dest, prev in reachableNodes:
            prevPrev = prev
            nextPrev = prev
            while nextPrev != self.id:
                prevPrev = nextPrev
                nextPrev = reachableNodes[prevPrev][1]
            routingTable[dest] = linkFromNode(prevPrev)

        # Start using the new routing table.
        self.routingTable = routingTable

        # Reset the routers that exist (allows for changing network... as long as
        # it doesn't change during an updating period)
        self.allRouters = set()
        self.knownNodes = set()
        # Reset the all costs table to know nothing
        self.allCostsTable = []

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
        # A dictionary of {nodeID: (cost, isHost)}
        # Could be more efficient
        costs = {}
        for link in self.links:
            cost = 5 * link.bufferUsed / link.bufferSize + link.propagationDelay
            costs[link.destination.id] = (cost, link.destination.type == 'host')

        # Data is of form (from, {to: (cost, isHost)}),
        # where from is self.id.
        data = (self.id, copy(costs))
        packet = Routing(self.id, data)

        # Send the packet to all neighbors
        for link in self.links:
            link.put(packet)

        # Update the all costs table to include my own costs
        self.addToAllCosts(data)

    def addToAllCosts(self, data):
        '''
        Takes data in the form (from, {to: cost}), and adds this info to
        self.allCostsTable.
        '''
        for to, (cost, isHost) in data[1].items():
            self.allCostsTable.append((data[0], to, cost))

        # Update known/unknown nodes
        # Add newly discovered routers to our info.
        # packet.data[1] has both cost info (index 0) and isHost (bool, index 1)
        newRouters = set([i[0] for i in data[1] if not i[1]])
        # Combine all routers found with the recently discovered routers
        self.allRouters = self.allRouters | newRouters
        # Update the nodes we have info about (we just got a new packet's data)
        self.knownNodes.add(data[0])
