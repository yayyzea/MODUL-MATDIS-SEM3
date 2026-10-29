"""
Radio station graph model (Graph Coloring + Connected Components)
Runs in Thonny with the standard library only (tkinter is bundled with Python).
"""

import math
import tkinter as tk

# ---------------------------------------------------------------------------
# 1. Graph model: vertices = stations, edges = adjacent stations (< 10 km)
# ---------------------------------------------------------------------------
STATIONS = ["A", "B", "C", "D", "E", "F", "G", "H"]

ADJACENCY = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "E"],
    "D": ["B", "F"],
    "E": ["C", "G"],
    "F": ["D", "H"],
    "G": ["E", "H"],
    "H": ["F", "G"],
}


def build_edges(adjacency):
    """Return the undirected edge list (each edge appears once)."""
    edges = set()
    for u, neighbours in adjacency.items():
        for v in neighbours:
            edges.add(tuple(sorted((u, v))))
    return sorted(edges)


def check_symmetry(adjacency):
    """Confirm that every adjacency is listed from both sides."""
    for u, neighbours in adjacency.items():
        for v in neighbours:
            if u not in adjacency[v]:
                return False
    return True


# ---------------------------------------------------------------------------
# 2. Connected components (depth-first search)
# ---------------------------------------------------------------------------
def connected_components(vertices, adjacency):
    visited = set()
    components = []
    for start in vertices:
        if start in visited:
            continue
        stack = [start]
        component = []
        visited.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            for nb in adjacency[node]:
                if nb not in visited:
                    visited.add(nb)
                    stack.append(nb)
        components.append(sorted(component))
    return components


# ---------------------------------------------------------------------------
# 3. Graph coloring and chromatic number (exact, via backtracking)
# ---------------------------------------------------------------------------
def try_coloring(vertices, adjacency, k):
    """Try to color the graph with k colors (1..k). Return dict or None."""
    coloring = {}

    def backtrack(index):
        if index == len(vertices):
            return True
        v = vertices[index]
        for color in range(1, k + 1):
            if all(coloring.get(nb) != color for nb in adjacency[v]):
                coloring[v] = color
                if backtrack(index + 1):
                    return True
                del coloring[v]
        return False

    return coloring if backtrack(0) else None


def chromatic_number(vertices, adjacency):
    """Smallest k for which a valid coloring exists."""
    for k in range(1, len(vertices) + 1):
        result = try_coloring(vertices, adjacency, k)
        if result is not None:
            return k, result
    return None, None


def is_valid_coloring(edges, coloring):
    return all(coloring[u] != coloring[v] for u, v in edges)


# ---------------------------------------------------------------------------
# 4. Visualization with tkinter
# ---------------------------------------------------------------------------
COLOR_PALETTE = {
    1: "#AFA9EC",  # frequency 1 (purple)
    2: "#5DCAA5",  # frequency 2 (teal)
    3: "#F0997B",
    4: "#EF9F27",
}

# Placement order around the circle, chosen so the ring shape is visible
# (this only affects how the graph is drawn, not the graph itself).
DRAW_ORDER = ["A", "B", "D", "F", "H", "G", "E", "C"]


def draw_graph(edges, coloring, k):
    root = tk.Tk()
    root.title("Radio stations graph - chromatic number = " + str(k))

    size = 560
    canvas = tk.Canvas(root, width=size, height=size + 50, bg="white")
    canvas.pack()

    cx, cy, radius, node_r = size / 2, size / 2, 200, 26
    positions = {}
    for i, name in enumerate(DRAW_ORDER):
        angle = -math.pi / 2 + i * 2 * math.pi / len(DRAW_ORDER)
        positions[name] = (cx + radius * math.cos(angle),
                           cy + radius * math.sin(angle))

    for u, v in edges:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        canvas.create_line(x1, y1, x2, y2, width=2, fill="#444444")

    for name, (x, y) in positions.items():
        fill = COLOR_PALETTE.get(coloring[name], "#cccccc")
        canvas.create_oval(x - node_r, y - node_r, x + node_r, y + node_r,
                           fill=fill, outline="#333333", width=2)
        canvas.create_text(x, y, text=name, font=("Arial", 16, "bold"))

    # Legend
    legend_y = size + 20
    start_x = size / 2 - 40 * k - 20
    for c in range(1, k + 1):
        x = start_x + (c - 1) * 150
        canvas.create_oval(x, legend_y - 10, x + 20, legend_y + 10,
                           fill=COLOR_PALETTE.get(c, "#cccccc"),
                           outline="#333333")
        canvas.create_text(x + 28, legend_y, text="Frequency " + str(c),
                           anchor="w", font=("Arial", 11))

    root.mainloop()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    edges = build_edges(ADJACENCY)

    print("=== Graph model ===")
    print("Vertices:", STATIONS)
    print("Edges   :", edges)
    print("Number of edges:", len(edges))
    print("Adjacency symmetric:", check_symmetry(ADJACENCY))
    print("Degrees :", {v: len(ADJACENCY[v]) for v in STATIONS})

    print("\n=== Connected components ===")
    comps = connected_components(STATIONS, ADJACENCY)
    print("Number of components:", len(comps))
    for i, comp in enumerate(comps, start=1):
        print("  Component", i, ":", comp)

    print("\n=== Graph coloring ===")
    k, coloring = chromatic_number(STATIONS, ADJACENCY)
    print("Chromatic number chi(G) =", k)
    print("Valid coloring:", is_valid_coloring(edges, coloring))
    for c in range(1, k + 1):
        group = [v for v in STATIONS if coloring[v] == c]
        print("  Frequency", c, ":", group)

    draw_graph(edges, coloring, k)


if __name__ == "__main__":
    main()
