import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(G, title, pos=None, node_colors='skyblue'):
    plt.figure(figsize=(10, 7))
    if pos is None:
        if isinstance(G, nx.DiGraph):
            pos = nx.spring_layout(G, k=0.6, seed=60)
        else:
            pos = nx.spring_layout(G, k=0.6, seed=60)

    # Menggambar semua simpul
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=400)
    
    # Menggambar semua sisi
    nx.draw_networkx_edges(G, pos, edge_color='gray')

    # Menggambar label
    nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")
    
    plt.title(title)
    plt.axis('off')
    plt.show()


edges_ui = [('Dian Sastrowardoyo', 'Najwa Shihab'), 
            ('Dian Sastrowardoyo', 'Raditya Dika'), 
            ('Raditya Dika', 'Sheila Dara')]
edges_itb = [('Ridwan Kamill', 'Devina Hermawan'), 
             ('Devina Hermawan', 'Joko Anwar'),
             ('Ridwan Kamill', 'Sujiwo Tejo')]  
edges_ugm = [('Marissa Haque', 'Ifan Seventeen'), 
             ('Ikang Fauzi', 'Ifan Seventeen'),
             ('Marissa Haque', 'John Tobing')]
edges_unpad = [('Ananda Omesh', 'Yura Yunita'), 
                ('Yura Yunita', 'Uus'),
                ('Ananda Omesh','Alshad Ahmad')]

G_disconnected = nx.Graph()
G_disconnected.add_edges_from(edges_ui + edges_itb + edges_ugm + edges_unpad)

colors = []
for node in G_disconnected.nodes():
    if any(node in edge for edge in edges_ui):
        colors.append('pink')          
    elif any(node in edge for edge in edges_itb):
        colors.append('lightblue')     
    elif any(node in edge for edge in edges_ugm):
        colors.append('lightgreen')   
    else:
        colors.append('orange')

print(f"Jumlah komponen terhubung: {nx.number_connected_components(G_disconnected)}\n")
print(f"Komponen terhubung: {list(nx.connected_components(G_disconnected))}\n")
print("Daftar simpul tiap komponen:")
for component in nx.connected_components(G_disconnected):
    if 'Dian Sastrowardoyo' in component:
        nama_kampus = "UI"
    elif 'Ridwan Kamill' in component:
        nama_kampus = "ITB"
    elif 'Marissa Haque' in component:
        nama_kampus = "UGM"
    else:
        nama_kampus = "UNPAD"
    print(f"Komponen {nama_kampus}: {list(component)}")

visualize_graph(G_disconnected, "Graf Tidak Terhubung", node_colors=colors) # type: ignore
