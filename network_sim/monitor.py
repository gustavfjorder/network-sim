# For graphing at the end
import matplotlib.pyplot as plt
# Fixes weird mac error for Alix
"""
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
"""

# For excel
import pandas as pd
import numpy as np

def show_results(monitor):
    for i, link in enumerate(monitor.links):
        plt.plot(monitor.linkRates[i])
        plt.show()

        plt.plot(monitor.linkBufferUsed[i])
        plt.show()

    for i, flows in enumerate(monitor.flows):
        plt.plot(monitor.flowWindowSize[i])
        plt.show()

def export_results(monitor, new_filename = "output.xlsx"):
    writer = pd.ExcelWriter(new_filename, engine='xlsxwriter')

    for i, link in enumerate(monitor.links):
        array = np.array([list(range(len(monitor.linkRates))), \
                        monitor.linkRates[i], \
                        monitor.linkBufferUsed[i], \
                        monitor.linkPacketsDropped[i]])
        df = pd.DataFrame(array)
        df.to_excel(writer, sheet_name = link.id)

    for i, flow in enumerate(monitor.flows):
        array = np.array([list(range(len(monitor.flowWindowSize))), \
                        monitor.flowWindowSize[i], \
                        monitor.flowRTT[i]])
        df = pd.DataFrame(array)
        df.to_excel(writer, sheet_name = flow.id)

    writer.save()


class Monitor:
    def __init__(self, env, links, flows):
        self.env = env
        self.links = links
        self.flows = flows
        self.refreshRate = 10  # ms

        # Initialize a place to store link info
        self.linkRates = [[] for i in range(len(links))]
        self.linkBufferUsed = [[] for i in range(len(links))]
        self.linkPacketsDropped = [[] for i in range(len(links))]

        # Initialize flow info
        self.flowWindowSize = [[] for i in range(len(flows))]
        self.flowRTT = [[] for i in range(len(flows))]

        # Start simpy process
        self.env.process(self.run())

    def run(self):
        while True:
            print("monitor")
            self.checkLinks()
            self.checkFlows()

            # Wait another ms, then check again
            yield self.env.timeout(self.refreshRate)

    def checkLinks(self):
        for i, link in enumerate(self.links):
            # Get the number of bits sent recently, then reset
            linkRate = link.bitsSent / (self.refreshRate * 10**-3) # bps
            link.bitsSent = 0
            self.linkRates[i].append(linkRate)

            bufferUsed = link.bufferUsed
            self.linkBufferUsed[i].append(bufferUsed)

            # Get the number of packets dropped, then reset
            packetsDropped = link.packetsDropped
            link.packetsDropped = 0
            self.linkPacketsDropped[i].append(packetsDropped)

    def checkFlows(self):
        for i, flow in enumerate(self.flows):
            # Get the current window size
            windowSize = flow.windowSize
            self.flowWindowSize[i].append(windowSize)

            # Get the current round trip time
            RTT = flow.RTT
            self.flowRTT[i].append(RTT)
