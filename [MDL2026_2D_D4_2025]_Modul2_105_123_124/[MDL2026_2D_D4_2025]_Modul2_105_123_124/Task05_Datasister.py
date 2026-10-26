import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# inisiasi graf
G = nx.DiGraph()

# menambahkan nodes
nodes = ["Processor", "Memory", "Storage", "Network Interface"]
G.add_nodes_from(nodes)

# menambahkan edges
edges_G = [('Processor', 'Memory'), ('Processor', 'Storage'), 
           ('Memory', 'Processor'), ('Storage', 'Network Interface'), 
           ('Network Interface', 'Processor')]
G.add_edges_from(edges_G)

# Menghitung dan menampilkan properti graf
print("\n--- Analisis Directed Graf Datasister ---")
print(f"Jumlah nodes: {G.number_of_nodes()}")
print(f"Jumlah edges: {G.number_of_edges()}")
print("Derajat masuk dan derajat keluar setiap node:")
for node in G.nodes():
    print(f"  - Nodes '{node}': in = {G.in_degree[node]}, out = {G.out_degree[node]}")

#Adj List
print("\nAdjacency List:")
for node in G.nodes():
    neighbors = []
    for u, v in G.edges():
        if u == node:
            neighbors.append(v)
    print(f"{node}: {neighbors}")

#Adj Matrix
nodelist = sorted(list(G.nodes()))
adj_matrix = nx.to_numpy_array(G, nodelist=nodelist)
print("\nAdjacency Matrix:")
print(adj_matrix)

# Handshaking Theorem (Graf Berarah)
total_in_degree = sum(dict(G.in_degree()).values())
total_out_degree = sum(dict(G.out_degree()).values())
jumlah_sisi = G.number_of_edges()

print("\nVerifikasi Handshaking Theorem (Graf Berarah):")
print(f"Total in-degree = {total_in_degree}")
print(f"Total out-degree = {total_out_degree}")
print(f"Jumlah sisi = {jumlah_sisi}")

if total_in_degree == jumlah_sisi and total_out_degree == jumlah_sisi:
    print("Status: TERVERIFIKASI (Handshaking Theorem terbukti benar)")
else:
    print("Status: TIDAK TERVERIFIKASI")

#Isomorfisme
# G4: BUKAN isomorfik (in-degree simpul c = 3, sedangkan G maksimal 2)
G4 = nx.DiGraph()
G4.add_edges_from([('a', 'b'), ('a', 'c'), ('b', 'c'), ('d', 'c'), ('d', 'a')])

# G5: isomorfik (struktur sama, hanya nama simpul berbeda)
G5 = nx.DiGraph()
G5.add_edges_from([('a', 'b'), ('a', 'c'), ('b', 'a'), ('c', 'd'), ('d', 'a')])

print("\nIsomorfisme:")
print(f"G isomorfik dengan G4: {nx.is_isomorphic(G, G4)}")
print(f"G isomorfik dengan G5: {nx.is_isomorphic(G, G5)}")

matcher = nx.isomorphism.DiGraphMatcher(G, G5)
if matcher.is_isomorphic():
    print("Pemetaan simpul G -> G5:", matcher.mapping)

# Memvisualisasikan graf
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color="lightblue",
        node_size=5500, font_size=10, font_weight="bold",
        edge_color="gray", connectionstyle="arc3,rad=0.05")
plt.title("Datasister")
plt.show()