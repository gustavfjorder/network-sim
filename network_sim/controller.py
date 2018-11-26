import simpy
import interface
import sys
from monitor import Monitor, show_results, export_results
import simpy.util


def runSimulator(input_file):

    env = simpy.Environment()

    debug = True

    hosts, links, flows, routers = interface.get_config(env, input_file, debug)

    monitor = Monitor(env, links, flows)

    # Run the simulation
    env.run(10 * 1000)

    # Graph the results
    show_results(monitor)

    # Export the resutls to output.xlsx
    export_results(monitor)

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Usage: <jsonFilename>")
    else:
        runSimulator(sys.argv[1])
