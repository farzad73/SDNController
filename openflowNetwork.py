import networkx as nx
import matplotlib.pyplot as plt


class MultiGraph(nx.MultiGraph):

    def __init__(self, **attr):
        super().__init__(**attr)
        self.node = {}
        self.edge = {}

    def add_node(self, node, attr_dict=None, **attrs):
        attr_dict = {} if attr_dict is None else attr_dict
        attr_dict.update(attrs)
        self.node[node] = attr_dict

    def add_edge(self, src, dst, key=None, attr_dict=None, **attrs):
        """Add edge to graph
           key: optional key
           attr_dict: optional attribute dict
           attrs: more attributes
           warning: udpates attr_dict with attrs"""
        attr_dict = {} if attr_dict is None else attr_dict
        attr_dict.update(attrs)
        self.node.setdefault(src, {})
        self.node.setdefault(dst, {})
        self.edge.setdefault(src, {})
        self.edge.setdefault(dst, {})
        self.edge[src].setdefault(dst, {})
        entry = self.edge[dst][src] = self.edge[src][dst]
        # If no key, pick next ordinal number
        if key is None:
            keys = [k for k in entry.keys() if isinstance(k, int)]
            key = max([0] + keys) + 1
        entry[key] = attr_dict
        return key

    def nodes(self, data=False):
        """Return list of graph nodes"""
        return self.node.items() if data else self.node.keys()

    def edges_iter(self, data=False, keys=False):
        """Iterator: return graph edges"""
        for src, entry in self.edge.items():
            for dst, keys in entry.items():
                if src > dst:
                    # Skip duplicate edges
                    continue
                for k, attrs in keys.items():
                    if data:
                        if keys:
                            yield (src, dst, k, attrs)
                        else:
                            yield (src, dst, attrs)
                    else:
                        if keys:
                            yield (src, dst, k)
                        else:
                            yield (src, dst)

    def edges(self, data=False, keys=False):
        """Return list of graph edges"""
        return list(self.edges_iter(data=data, keys=keys))

    def __getitem__(self, node):
        """Return link dict for given src node"""
        return self.edge[node]

    def __len__(self):
        """Return the number of nodes"""
        return len(self.node)

    def convertTo(self, cls, data=False, keys=False):
        """Convert to networkx.MultiGraph"""
        g = cls()
        g.add_nodes_from(self.nodes(data=data))
        g.add_edges_from(self.edges(data=(data or keys), keys=keys))
        return g


class Topo(object):

    def __init__(self):
        self.g = MultiGraph()
        self.hopts = {}
        self.sopts = {}
        self.lopts = []
        # ports[src][dst][sport] is port on dst that connects to src
        self.ports = {}

    def showGraph(self):
        """Drawing graph"""
        g = self.g.convertTo(nx.MultiGraph)
        nx.draw(g, with_labels=True)
        plt.show()

    def shortestPath(self):
        """Compute the shortest paths of graph"""
        sps = nx.shortest_path(self.g.convertTo(nx.MultiGraph))
        shortest_paths = []
        for source in sps:
            if source in self.hosts():
                for destination in sps[source]:
                    if destination != source and destination in self.hosts():
                        shortest_paths.append(sps[source][destination])
        return shortest_paths

    def addNode(self, name, **opts):
        self.g.add_node(name, **opts)
        return name

    def addHost(self, name, **opts):
        self.hopts[name] = opts
        self.hopts[name]['ports'] = {}
        return self.addNode(name, **opts)

    def addSwitch(self, name, **opts):
        self.sopts[name] = {}
        result = self.addNode(name, isSwitch=True, **opts)
        return result

    def addLink(self, node1, node2, port1=None, port2=None, key=None, **opts):
        """node1, node2: nodes to link together
           port1, port2: ports (optional)
           opts: link options (optional)
           returns: link info key"""
        port1, port2 = self.addPort(node1, node2, port1, port2)
        opts = dict()
        opts.update(node1=node1, node2=node2, port1=port1, port2=port2)
        self.g.add_edge(node1, node2, key, **opts)
        self.lopts.append(opts)
        return key

    def addPort(self, src, dst, sport=None, dport=None):
        """
            Generate port mapping for new edge.
                src: source switch name
                dst: destination switch name
        """

        # Initialize if necessary
        ports = self.ports
        ports.setdefault(src, {})
        ports.setdefault(dst, {})
        # New port: number of outlinks + base
        if sport is None:
            src_base = 1 if self.isSwitch(src) else 0
            sport = len(ports[src]) + src_base
        if dport is None:
            dst_base = 1 if self.isSwitch(dst) else 0
            dport = len(ports[dst]) + dst_base
        ports[src][sport] = (dst, dport)
        ports[dst][dport] = (src, sport)

        self.sopts[src].update(ports[src]) if self.isSwitch(src) else self.hopts[src]['ports'].update(ports[src])
        self.sopts[dst].update(ports[dst]) if self.isSwitch(dst) else self.hopts[dst]['ports'].update(ports[dst])

        return sport, dport

    def isSwitch(self, n):
        """Returns true if node is a switch."""
        return self.g.node[n].get('isSwitch', False)

    def nodes(self):
        """Return nodes in graph"""
        return self.g.nodes()

    def switches(self):
        """Return switches"""
        return [n for n in self.nodes() if self.isSwitch(n)]

    def hosts(self):
        """Return hosts"""
        return [n for n in self.nodes() if not self.isSwitch(n)]


if __name__ == '__main__':
    net = Topo()
    s1 = net.addSwitch('s1')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    h2 = net.addHost('h2', ip='10.0.0.2')
    h5 = net.addHost('h5', ip='10.0.0.5')
    h1 = net.addHost('h1', ip='10.0.0.1')
    h4 = net.addHost('h4', ip='10.0.0.4')
    h3 = net.addHost('h3', ip='10.0.0.3')

    net.addLink(s1, s2)
    net.addLink(s2, s4)
    net.addLink(s2, s5)
    net.addLink(s5, s3)
    net.addLink(h4, s1)
    net.addLink(s2, h5)
    net.addLink(s3, h3)
    net.addLink(s5, h2)
    net.addLink(s4, h1)


    print(net.sopts)
    print(net.hopts)