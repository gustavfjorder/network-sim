#import notes
import json

def get_config(filename):
# Takes filename (json) file and outputs a list of hosts, routers, links, flows.
    try:
        with open(filename) as f:
            data = json.load(f)
    except FileNotFoundError as error:
        print("File not found")
        data = None
    return data

def main():
    input_file = input("Test name: ")
    test_data = get_config(input_file)
    if test_data != None:
        print(test_data)

if __name__ == "__main__":
    main()
