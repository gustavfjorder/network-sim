#import notes
import json

def get_config(env,filename):
# Takes filename (json) file and outputs a list of hosts, routers, links, flows.
    try:
        with open(filename) as f:
            test_data = json.load(f)
    except FileNotFoundError as error:
        print("File not found")
        test_data = None
        return

    hosts = []
    links = []
    flows = []
    for host in test_data['hosts']:
        host = Host(env, test_data['hosts'][host]['host_id'],1)
        hosts.append(host)

    # create link objects
    for link in test_data["links"]:
        link = Link(env, \
        test_data['links'][link]['link_id'],\
        test_data['links'][link]['link_delay'], \
        test_data['links'][link]['link_buffer'], \
        test_data['links'][link]['link_rate'])
        links.append(link)

    # create flow objects
    for flow in test_data['flows']:
        flow = Flow(\
        test_data['flows'][flow]['flow_src'],\
        test_data['flows'][flow]['flow_dest'],\
        test_data['flows'][flow]['data_amt'],\
        test_data['flows'][flow]['flow_start'])
        flows.append(flow)

    return hosts,links,flows


def main():
    env = 0 
    input_file ="test0.json"#{} input("Test name: ")
    test_data = get_config(env,input_file)



if __name__ == "__main__":
    main()
