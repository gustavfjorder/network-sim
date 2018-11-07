import simpy
import interface
import sys
from monitor import Monitor, show_results, export_results


def runSimulator(input_file):

    env = simpy.Environment()

    # Initialize the functions
    # This will initialize any startup processes needed
    # Though we might need to change this if a flow starts after time 0
    hosts, links, flows = interface.get_config(env, input_file)

    monitor = Monitor(env, links, flows)
    env.process(monitor.run())

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
