#import notes
import json
from pprint import pprint



def get_config(filename):
# Takes filename (json) file and outputs a list of hosts, routers, links, flows.
# The lists are lists of objects.

    with open(filename) as f:
        data = json.load(f)

    pprint(data)

def main():
    get_config("test0.json")

if __name__ == "__main__":
    main()
