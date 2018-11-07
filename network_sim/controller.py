import simpy
import interface
import sys
from monitor import Monitor, show_results, export_results


def runSimulator(input_file):

    env = simpy.Environment()

    hosts, links, flows = interface.get_config(env, input_file)

    for link in links:
        env.process(link.run())

    for flow in flows:
        env.process(flow.run())

    monitor = Monitor(links, flows)

    # Run the simulation
    env.run()

    # Graph the results
    show_results(monitor)

    # Export the resutls to output.xlsx
    export_results(monitor)

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Usage: <jsonFilename>")
    else:
        runSimulator(sys.argv[1])
