import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Inisiasi graf
G1 = nx.Graph()

# Node
a = 'Soekarno-Hatta'
b = 'Jl. Asia Afrika'
c = 'Jl. Sunda'
d = 'Jl. Sunda-Karapitan'
e = 'Jl. Gatot Subroto'
f = 'Jl. Ahmad Yani'

N1 = [a, b, c, d, e, f]
G1.add_nodes_from(N1)

# Edge
E1 = [(a, b), (a, c), (a, d), (a, e), (a, f)]
G1.add_edges_from(E1)

print(G1)
print(E1)

# Visualisasi Graph Sederhana Bipartite
plt.figure(figsize=(8, 8))
pos = {a: (3, 3), b: (0, 3), c: (3, 6), d: (3, 0), e: (6, 3), f: (6, 6)}
nx.draw(G1, pos=pos, with_labels=True, node_color='lightblue', font_weight='bold', font_size=12, node_size=700)
plt.title("Visualisasi Graf Sederhana G1")
plt.show()