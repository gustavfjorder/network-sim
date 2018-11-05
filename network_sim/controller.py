import simpy
import interface
from monitor import Monitor, show_results


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
