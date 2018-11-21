from link import Link
from flow import Tahoe
from hosts import Host
from routers import Router
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
    routers = []
    links = []
    flows = []
    nodes = []

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
        f = Tahoe(id, env, source, flow_info['flow_dest'], flow_info['data_amt'], flow_info['flow_start'])

        flows.append(f)

    # create routers
    for router in test_data['routers']:
        router_info = test_data['routers'][router]

        id = router_info['router_id']

        links_list = router_info['links']
        router_links = [l for l in links if l.id in links_list \
                                    and l.source == router_info['router_id']]
        r = Router(env, id, router_links)

        routers.append(r)

    # Add source/destination obejcts to links, replacing string IDs
    nodes = routers + hosts
    for link in links:
        source = next((n for n in nodes if n.id == link.source), None)
        destination = next((n for n in nodes if n.id == link.destination), None)
        link.source = source
        link.destination = destination

    return (hosts, links, flows, routers)
