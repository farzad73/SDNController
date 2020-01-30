from openflowNetwork import Topo

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

# print(net.shortestPath())
# print(net.hopts)
# print(net.sopts)


for sp in net.shortestPath():
    print(sp)
    src = sp[0]
    dst = sp[-1]
    sp.remove(src)
    sp.remove(dst)

    rule = {
        "actions": [],
        "priority": 65535,
        "duration_sec": 0,
        "match": {
            "dst": net.hopts[src],
            "src": net.hopts[dst],
            "in_port": 3
        }
    }

    for i in range(0, len(sp)):
        opts = net.sopts[sp[i]]
        for key in opts:
            if opts[key][0] == src:
                rule['match']['in_port'] = key

    for switch in sp:
        print(switch + ' --> ' + str(net.sopts[switch]))



