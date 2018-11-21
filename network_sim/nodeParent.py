# class that both routers and hosts inherit from

class nodeParent():
    def __init__(self, env, name, links):
        self.env = env
        self.id = name
        self.links = links
        self.type = None;

    def put(self, packet):
        # will be overwritten by hosts or routers
        pass

    def send (self, packet):
        # will be overwritten by hosts or routers
        pass
