from link import Link
from flow import Tahoe
from hosts import Host
import json

# Takes filename (json) file and outputs a list of hosts, routers, links, flows.
def get_config(env,filename):
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

    # create link objects
    for link in test_data["links"]:
        link_info = test_data['links'][link]
        l = Link(env, \
        link_info['link_id'],\
        link_info['link_delay'], \
        link_info['link_buffer'], \
        link_info['link_rate'], \
        link_info['link_source'], \
        link_info['link_destination'])
        links.append(l)

    # create hosts
    for host in test_data['hosts']:
        host_info = test_data['hosts'][host]
        link = next((l for l in links if l.id == test_data['hosts'][host]['link_id'] \
                                    and l.source == host_info['host_id']), None)
        h = Host(env, host_info['host_id'], link)
        hosts.append(h)

    # create flow objects
    # TODO: Start of flows changes
    for flow in test_data['flows']:
        flow_info = test_data['flows'][flow]

        id = flow_info['flow_id']
        source = next((h for h in hosts if h.id == flow_info['flow_src']), None)

        f = Tahoe(id, env, source, flow_info['flow_dest'], flow_info['data_amt'])

        flows.append(f)

    # create routers
    for router in test_data['routers']:
        router_info = test_data['routers'][router]

        id = router_info['router_id']

        links_list = router_info['links']
        router_links = next((l for l in links if l.id in links_list \
                                    and l.source == router_info['router_id']), None)
        r = Router(env, id, links_list)

    # Add source/destination obejcts to links, replacing string IDs
    for link in links:
        source = next((h for h in hosts if h.id == link.source), None)
        destination = next((h for h in hosts if h.id == link.destination), None)
        link.source = source
        link.destination = destination

    print(hosts, links, flows)
    return (hosts, links, flows, router)



def main():
    env = 0
    input_file ="test0.json"#{} input("Test name: ")
    test_data = get_config(env,input_file)



if __name__ == "__main__":
    main()
