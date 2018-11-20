import simpy
import interface
import sys
from monitor import Monitor, show_results, export_results
import simpy.util


def runSimulator(input_file):

    env = simpy.Environment()

    hosts, links, flows, routers = interface.get_config(env, input_file)

    for link in links:
        env.process(link.run())

    for flow in flows:
        simpy.util.start_delayed(env, \
                             flow.run(), \
                             5000)

    monitor = Monitor(links, flows)

    # Run the simulation
    env.run(5000)

    # Graph the results
    #show_results(monitor)

    # Export the resutls to output.xlsx
    export_results(monitor)

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Usage: <jsonFilename>")
    else:
        runSimulator(sys.argv[1])
