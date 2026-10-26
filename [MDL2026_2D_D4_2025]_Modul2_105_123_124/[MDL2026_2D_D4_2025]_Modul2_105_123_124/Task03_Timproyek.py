import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Inisiasi graf
G1 = nx.Graph()

# Node
a = 'Alyn'
b = 'Betty'
c = 'Carol'
d = 'David'
e = 'UI/UX'
f = 'Backend'
g = 'Database'
h = 'Testing'

N1 = [a, b, c, d, e, f, g, h]
G1.add_nodes_from(N1)

# Edge
E1 = [(a, e), (a, h), (b, e), (b, f), (c, e), (c, g), (d, f), (d, h)]
G1.add_edges_from(E1)

print(G1)
print(E1)

# Visualisasi Graph Sederhana Bipartite
plt.figure(figsize=(6, 6))
pos = {a: (0, 1), b: (1, 1), c: (2, 1), d: (3, 1), e: (0, 2), f: (1, 2), g: (2, 2), h: (3, 2)}
nx.draw(G1, pos=pos, with_labels=True, node_color='lightblue', font_weight='bold', font_size=12, node_size=700)
plt.title("Visualisasi Graf Sederhana G1")
plt.show()

# Adjacency List
adj_list = nx.to_dict_of_lists(G1)
print("\nAdjacency List:")
print(adj_list)

# Adjacency Matrix
nodelist = sorted(list(N1))
adj_matrix = nx.to_numpy_array(G1, nodelist=nodelist)
print("\nAdjacency Matrix:")
print(adj_matrix)
    
# Derajat SImpul
print("\nDerajat Tiap Node")
for node in G1.nodes():
    print(f"  - Nodes '{node}': {G1.degree[node]}")
    
# Handshaking
degrees = dict(G1.degree())
total_derajat = sum(degrees.values())
jumlah_sisi = G1.number_of_edges()
print(f"Total derajat semua simpul = {total_derajat}")
print(f"2 * Jumlah Sisi (2 * {jumlah_sisi}) = {2 * jumlah_sisi}")

if total_derajat == (2 * jumlah_sisi):
    print("Status: TERVERIFIKASI (Handshaking Theorem terbukti benar)")
else:
    print("Status: TIDAK TERVERIFIKASI")
    
# Isomorphic test
graf_khusus = {
    "Graf Lengkap (K8)": nx.complete_graph(8),
    "Graf Lingkaran (C8)": nx.cycle_graph(8),
    "Graf Lintasan (P8)": nx.path_graph(8),
    "Graf Bipartit Lengkap (K4,4)": nx.complete_bipartite_graph(4, 4),
    "Graf Roda (W7)": nx.wheel_graph(8),
    "Graf Kubus (Q3)": nx.hypercube_graph(3),
    "Graf Bintang (S7)": nx.star_graph(7),
}

ada_isomorfik = False
for nama_graf, G_khusus in graf_khusus.items():
    is_iso = nx.is_isomorphic(G1, G_khusus)
    print(f"Isomorfik dengan {nama_graf}?: {is_iso}")
    if is_iso:
        ada_isomorfik = True

if not ada_isomorfik:
    print("\n[KESIMPULAN]")
    print("Graf G1 TIDAK ISOMORFIK dengan graf khusus standar mana pun.")
    print(
        "Graf G1 adalah Graf Bipartit biasa (subgraf dari K4,4), bukan Graf Bipartit Lengkap."
    )
