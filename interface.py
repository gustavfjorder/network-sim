import notes
import json

def get_config(filename):
    # Takes filename (json) file and outputs a list of hosts, routers, links, flows.
    # The lists are lists of objects.

    file = open(filename)
    input = json.loads(file)

    # Close file
    file.close()
