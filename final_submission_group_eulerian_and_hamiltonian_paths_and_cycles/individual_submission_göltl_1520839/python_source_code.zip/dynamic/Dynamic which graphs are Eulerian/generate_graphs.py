import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import networkx as nx
import random
from gviz import nx_to_graphviz


def generate_eulerian_multigraph(max_edges=14):
    G = nx.MultiGraph()
    nodes = list(range(0, random.randint(6, 10)))
    num_edges = random.randint(len(nodes) + 3, max_edges)
    # start with graph of random edges
    for _ in range(num_edges):
        u, v = random.sample(nodes, 2)
        G.add_edge(u, v)

    # Remove random edge and add random edge until graph is eulerian
    while not nx.is_eulerian(G):
        u, v, k = random.choice(list(G.edges))
        G.remove_edge(u, v, k)
        u, v = random.sample(nodes, 2)
        G.add_edge(u, v)
    return G


def generate_non_eulerian_multigraph(max_edges=14):
    G = nx.MultiGraph()
    nodes = list(range(0, random.randint(6, 10)))
    num_edges = random.randint(len(nodes) + 3, max_edges)
    # Start with a cycle (Eulerian)
    edges = [(nodes[i], nodes[(i + 1) % len(nodes)]) for i in range(len(nodes))]
    G.add_edges_from(edges)

    # Add edges randomly to create odd degree nodes (non-Eulerian)
    while G.number_of_edges() < num_edges:
        u, v = random.sample(nodes, 2)
        G.add_edge(u, v)
        # Check if graph is non-Eulerian
        if nx.is_eulerian(G):
            # If still Eulerian, remove the edge to enforce non-Eulerian
            G.remove_edge(u, v)
        else:
            # Keep this edge as it causes non-Eulerian structure
            continue
    return G


# Generate 10 such Eulerian MultiGraphs
correct_graphs = [generate_eulerian_multigraph() for _ in range(10)]

# Verify that each graph is Eulerian
for i, g in enumerate(correct_graphs):
    assert nx.is_eulerian(g), f"Graph {i} is not Eulerian"

wrong_graphs = [generate_non_eulerian_multigraph() for _ in range(20)]

# Verify each graph is non-Eulerian
for i, g in enumerate(wrong_graphs):
    assert not nx.is_eulerian(g), f"Graph {i} is incorrectly Eulerian"

# Save graphs to Python file with constructor calls
def save_graphs_to_python_file(correct_graphs, wrong_graphs, filename='graphs.py'):
    with open(filename, 'w') as f:
        f.write("import networkx as nx\n\n")

        f.write("correct_graphs = [\n")
        for i, graph in enumerate(correct_graphs):
            edges = list(graph.edges())
            f.write(f"    nx.MultiGraph({edges}),  # Graph {i+1}\n")
        f.write("]\n\n")
        
        f.write("wrong_graphs = [\n")
        for i, graph in enumerate(wrong_graphs):
            edges = list(graph.edges())
            f.write(f"    nx.MultiGraph({edges}),  # Graph {i+1}\n")
        f.write("]\n\n")
        

# Save the graphs
save_graphs_to_python_file(correct_graphs, wrong_graphs)
