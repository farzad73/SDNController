import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter


#####################INPUT#####################
BUDGET = 4
NETWORK_GML = 'Cogentco.gml'

#####################PROCESS#####################
g = nx.read_gml(NETWORK_GML)

# positions = {}
# for node in g.nodes():
#     positions[node] = (g._node[node]['Latitude'], g._node[node]['Longitude'])
# nx.draw(g, positions, with_labels=True)
# plt.show()

sdn_nodes = []

bc = dict(nx.degree(g))
k = Counter(bc)
sdn_nodes = list(dict(k.most_common(4)).keys())

# while BUDGET > 0:
#     degrees = dict(nx.degree(g))
#     max_degree = max(degrees, key = degrees.get)
#     sdn_nodes.append(max_degree)
#     g.remove_node(max_degree)
#     BUDGET -= 1

    # nx.draw(g, positions, with_labels=True)
    # plt.show()

print(sdn_nodes)
#####################PROCESS#####################
g = nx.read_gml(NETWORK_GML)
sp_dic = nx.shortest_path(g)

sps = []

for source in sp_dic:
    for destination in sp_dic[source]:
        sps.append(sp_dic[source][destination])

counter = 0
for sp in sps:
    for node in sdn_nodes:
        if node in sp:
            counter += 1
            break

print(counter/len(sps))