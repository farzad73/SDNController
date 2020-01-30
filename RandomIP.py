class Network(object):

    def __init__(self):
        self.switches = {}
        self.hosts = {}

    def add_switch(self, name):
        self.switches[name] = Switch(name)

    def add_host(self, name, ip):
        self.hosts[name] = Host(name, ip)

    def add_link_between_switches(self, src, dst):
        self.switches[src].portsCounter += 1
        self.switches[dst].portsCounter += 1
        self.switches[src].ports[self.switches[src].portsCounter] = {'dport': self.switches[dst].portsCounter,
                                                                     'name': dst}
        self.switches[dst].ports[self.switches[dst].portsCounter] = {'dport': self.switches[src].portsCounter,
                                                                     'name': src}

    def add_link_between_host_and_switch(self, src, dst):
        self.hosts[src].portsCounter += 1
        self.switches[dst].portsCounter += 1
        self.hosts[src].ports[self.hosts[src].portsCounter] = {'dport': self.switches[dst].portsCounter, 'name': dst}
        self.switches[dst].ports[self.switches[dst].portsCounter] = {'dport': self.hosts[src].portsCounter, 'name': src}


class Switch(object):

    def __init__(self, name):
        self.name = name
        self.portsCounter = 0
        self.ports = {}
        self.table_dict = {}
        self.input_flows = []


class Host(object):

    def __init__(self, name, ip):
        self.portsCounter = 0
        self.name = name
        self.ports = {}
        self.ip = ip