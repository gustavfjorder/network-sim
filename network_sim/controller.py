import simpy
import interface
import sys
from monitor import Monitor, show_results, export_results
import simpy.util


def runSimulator(input_file):

    env = simpy.Environment()

<<<<<<< HEAD
    hosts, links, flows, routers = interface.get_config(env, input_file)
=======
    # Initialize the functions
    # This will initialize any startup processes needed
    # Though we might need to change this if a flow starts after time 0
    hosts, links, flows = interface.get_config(env, input_file)
>>>>>>> refs/remotes/origin/master

    monitor = Monitor(env, links, flows)

    # Run the simulation
    env.run(5000)

    # Graph the results
    show_results(monitor)

    # Export the resutls to output.xlsx
    export_results(monitor)

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Usage: <jsonFilename>")
    else:
        runSimulator(sys.argv[1])
