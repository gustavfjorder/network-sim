# For graphing at the end
import matplotlib.pyplot as plt

def show_results(monitor):
    for i, link in enumerate(monitor.links):
        plt.plot(monitor.linkRates[i])
        plt.show()

        plt.plot(monitor.linkBufferUsed[i])
        plt.show()

    for i, flows in enumerate(monitor.flows):
        plt.plot(monitor.flowWindowSize[i])
        plt.show()
        

class Monitor:
    def __init__(self, links, flows):
        self.links = links
        self.flows = flows
        self.refreshRate = 10  # ms

        # Initialize a place to store link info
        self.linkRates = [[] for i in range(len(links))]
        self.linkBufferUsed = [[] for i in range(len(links))]
        self.linkPacketsDropped = [[] for i in range(len(links))]

        # Initialize flow info
        self.flowWindowSize = [[] for i in range(len(flows))]

    def run():
        while True:
            self.checkLinks()
            self.checkFlows()

            # Wait another ms, then check again
            yield simpy.timeout(self.refreshRate)

    def checkLinks():
        for i, link in enumerate(links):
            # Get the number of bits sent recently, then reset
            linkRate = link.bitsSent / (self.refreshRate * 10**-3) # bps
            link.bitsSent = 0
            linkRates[i].append(linkRate)

            bufferUsed = link.bufferUsed
            linkBufferUsed[i].append(bufferUsed)

            # Get the number of packets dropped, then reset
            packetsDropped = link.packetsDropped
            link.packetsDropped = 0
            self.linkPacketsDropped[i].append(packetsDropped)

    def checkFlows():
        for i, flow in enumerate(flows):
            # Get the current window size
            windowSize = flow.windowSize
            flowWindowSize[i].append(windowSize)
