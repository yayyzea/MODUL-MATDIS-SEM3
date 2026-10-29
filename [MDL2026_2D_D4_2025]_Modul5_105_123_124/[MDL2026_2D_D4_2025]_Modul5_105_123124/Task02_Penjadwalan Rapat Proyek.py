"""Penjadwalan rapat proyek dengan graph coloring."""
"""
Nama: Ivanka Bunga Aulia
NIM: 251524105
Kelas: 2D D4
"""

from collections import deque
from itertools import combinations
from typing import Dict, Optional, Set, Tuple

import matplotlib.pyplot as plt
import networkx as nx


SUBTEAMS: Dict[str, Set[str]] = {
    "Sub-tim 1": {"Alyn", "Betty", "Erin"},
    "Sub-tim 2": {"Alyn", "Carol", "Frank"},
    "Sub-tim 3": {"Betty", "David"},
    "Sub-tim 4": {"Carol", "Erin", "Frank"},
    "Sub-tim 5": {"David", "Frank"},
}

COLOR_PALETTE = ("#F87171", "#60A5FA", "#34D399", "#FBBF24", "#A78BFA")


def build_graph(
    subteams: Dict[str, Set[str]],
) -> Dict[str, Set[str]]:
    """Hubungkan dua sub-tim jika memiliki setidaknya satu anggota yang sama."""
    graph = {name: set() for name in subteams}
    for first, second in combinations(subteams, 2):
        if subteams[first] & subteams[second]:
            graph[first].add(second)
            graph[second].add(first)
    return graph


def find_coloring_with_k_colors(
    graph: Dict[str, Set[str]], color_count: int
) -> Optional[Dict[str, int]]:
    """Cari pewarnaan valid dengan paling banyak color_count warna."""
    order = sorted(graph, key=lambda vertex: (-len(graph[vertex]), vertex))
    coloring: Dict[str, int] = {}

    def assign_color(index: int) -> bool:
        if index == len(order):
            return True

        vertex = order[index]
        neighbor_colors = {
            coloring[neighbor]
            for neighbor in graph[vertex]
            if neighbor in coloring
        }
        for color in range(1, color_count + 1):
            if color not in neighbor_colors:
                coloring[vertex] = color
                if assign_color(index + 1):
                    return True
                del coloring[vertex]
        return False

    if assign_color(0):
        return coloring
    return None


def find_chromatic_number(
    graph: Dict[str, Set[str]],
) -> Tuple[int, Dict[str, int]]:
    """Coba jumlah warna mulai dari satu hingga ditemukan solusi."""
    for color_count in range(1, len(graph) + 1):
        coloring = find_coloring_with_k_colors(graph, color_count)
        if coloring is not None:
            return color_count, coloring
    raise ValueError("Graf tidak memiliki pewarnaan yang valid.")


def is_bipartite(graph: Dict[str, Set[str]]) -> bool:
    """Periksa apakah simpul-simpul graf dapat diwarnai dengan dua warna."""
    colors: Dict[str, int] = {}
    for start in graph:
        if start in colors:
            continue
        colors[start] = 0
        queue = deque([start])

        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    queue.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False
    return True


def show_graph_visualizations(
    graph: Dict[str, Set[str]],
    coloring: Dict[str, int],
    color_count: int,
) -> None:
    """Tampilkan graf sebelum dan sesudah pewarnaan dalam jendela visualisasi."""
    visual_graph = nx.Graph(graph)
    positions = nx.spring_layout(visual_graph, seed=42)

    print("\nVisualisasi graf sebelum pewarnaan:")
    nx.draw(
        visual_graph,
        positions,
        with_labels=True,
        node_color="lightgrey",
        font_weight="bold",
    )
    plt.title("Graf Sebelum Diwarnai")
    plt.show()

    node_colors = [
        COLOR_PALETTE[coloring[vertex] - 1]
        for vertex in visual_graph.nodes()
    ]
    print("\nVisualisasi graf setelah pewarnaan:")
    nx.draw(
        visual_graph,
        positions,
        with_labels=True,
        node_color=node_colors,
        font_weight="bold",
    )
    plt.title(f"Graf Setelah Diwarnai ({color_count} warna)")
    plt.show()


def main() -> None:
    graph = build_graph(SUBTEAMS)
    chromatic_number, coloring = find_chromatic_number(graph)

    print("Simpul graf (sub-tim):")
    for subteam, members in SUBTEAMS.items():
        print(f"  {subteam}: {{{', '.join(sorted(members))}}}")

    print("\nSisi graf (sub-tim yang berbagi anggota):")
    for first, second in combinations(SUBTEAMS, 2):
        shared_members = SUBTEAMS[first] & SUBTEAMS[second]
        if shared_members:
            members = ", ".join(sorted(shared_members))
            print(f"  {first} -- {second} (anggota sama: {members})")

    print("\nDaftar ketetanggaan:")
    for subteam, neighbors in graph.items():
        print(f"  {subteam}: {', '.join(sorted(neighbors)) or '(tidak ada)'}")

    print(f"\nChromatic Number (chi(G)) = {chromatic_number}")
    print("Jadwal rapat minimum:")
    for color in range(1, chromatic_number + 1):
        scheduled = sorted(
            subteam for subteam, assigned_color in coloring.items()
            if assigned_color == color
        )
        print(f"  Slot {color}: {', '.join(scheduled)}")

    print(f"\nApakah graf bipartit? {'Ya' if is_bipartite(graph) else 'Tidak'}")
    print(
        "Alasannya: Sub-tim 2, Sub-tim 4, dan Sub-tim 5 membentuk "
        "segitiga (siklus ganjil), sehingga perlu sedikitnya tiga warna."
    )
    print(
        "Perbandingan: graph coloring umum memakai warna minimum agar "
        "simpul bertetangga berbeda warna. Graf bipartit adalah kasus "
        "khusus yang simpulnya dapat dibagi menjadi dua kelompok tanpa "
        "sisi di dalam kelompok (setara dengan dapat diwarnai dua warna). "
        "Karena graf ini memiliki segitiga dan chi(G) = 3, graf ini bukan "
        "bipartit."
    )

    show_graph_visualizations(graph, coloring, chromatic_number)


if __name__ == "__main__":
    main()