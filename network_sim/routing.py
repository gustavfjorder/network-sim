# Just one router will be running run_routingInfo. On trigger, it will start
# to send, which will trigger the rest.

# TODO: What if there's just one router. Will it end?
# TODO: Need to add a to a is 0?

# Simple copy of array/dict/set
from copy import copy

if (packet.type = "routing"):
    addRoutingTableInfo(packet)

def init():
    # given routing table
    # Connected nodes
    self.connectedNodes = {link.destination.id: link for link in self.links}

# Form "some node": (cost, next node). e.g. {"c": (4, "c"), "d": (6, "c")}
# We will need a way to correlate nodes with links.
self.routingTable = {}

# For during construction of routing table

# Elements in the allCostsTable are in the form (from, to, cost)
self.allCostsTable = []
# These are all the nodes in the graph that we know exist. Set so no duplicates.
self.allNodes = set()
# These are all the nodes that we have received cost info about
self.knownNodes = set()


self.refreshRoutingTime = 5000   # 5 sec, which is what the test cases do


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
    if packet.data[0] in self.knownNodes:

        # Add the packet to the all costs table and update lists of nodes that
        # exist in the network and nodes that we have costs from.
        # TODO: Only if we haven't already added it? Depends on how we forward packets.
        #       wouldn't break it but is inefficient and don't want to end up in
        #       infinite loop
        self.addToAllCosts(packet.data)

        # The node we haven't received costs from will be empty when we have
        # a full view of the network
        unknownNodes = self.allNodes - self.knownNodes

        # If we have all the info of all known routers, then run Dijkstra
        # Otherwise, wait until more packets have been received
        if not unknownNodes:
            createRoutingTable(self)

        # Pass on the info to all other nodes connected
        for link in self.links:
            link.put(packet)


# Called when we have all knowledge of the graph to construct a shortest path
def createRoutingTable(self):
    # Run Dijkstra
    routingTable = []
    reachableNodes = set()

    while reachableNodes != self.allNodes:
        pass

    # Start using the new routing table.
    self.routingTable = routingTable

    # Reset the routers that exist (allows for changing network... as long as
    # it doesn't change during an updating period)
    self.allNodes = set()
    self.knownNodes = set()
    # Reset the all costs table to know nothing
    self.allCostsTable = []


# Inititalizes another round of routing every refreshRoutingTime, which will
# trigger a refresh for all connected routers.
# Only one router in the network needs to run this, though many could run it.
def run_routingInfo(self):
    while True:
        # Initialize a new routing cycle
        self.sendMyInfo(self)

        # Wait some time
        yield env.timeout(refreshRoutingTime)

# Helper functions

def myCosts(self):
    # Could be more efficient
    costs = {}
    for link in self.links:
        cost = 5 * link.bufferUsed / link.bufferSize + link.propagationDelay
        costs[link.id.destination] = cost

def sendMyInfo(self):

    # Refresh the router's costs
    costs = self.myCosts(self)

    #  Data is of form (from, {to: cost})
    data = (self.id, copy(costs))
    type = "routing"
    packet = Packet()

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
    for to, cost in data[1].items:
        self.allCostsTable.append((data[0], to, cost))

    # Update known/unknown nodes
    # We may have already known about these, but we may not have.
    newNodes = set(packet.data[1].values()):
    # Combine all nodes found with the recently discovered nodes
    self.allNodes = self.allNodes | newNodes
    # Update the nodes we have info about (we just got a new packet's data)
    self.knownNodes.add(packet.data[0])

def linkFromNode(self, node):
    '''
    Returns a connected link object that has node at the other side
    or None if the node isn't connected directly.
    '''
    if node in self.connectedNodes:
        return self.connectedNodes[node]
    else:
        return None
