import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import networkx as nx
import random
from gviz import nx_to_graphviz

def has_eulerian_path(graph):
    return sum([degree[1] % 2 for degree in graph.degree()]) == 2 or nx.is_eulerian(graph)

def generate_eulerian_path_multigraph(max_edges=14):
    G = nx.MultiGraph()
    nodes = list(range(0, random.randint(6, 10)))
    num_edges = random.randint(len(nodes) + 3, max_edges)
    for _ in range(num_edges):
        u, v = random.sample(nodes, 2)
        G.add_edge(u, v)

    while not has_eulerian_path(G):
        u, v, k = random.choice(list(G.edges))
        G.remove_edge(u, v, k)
        u, v = random.sample(nodes, 2)
        if random.random() < 0.1:
            u = len(nodes)
        G.add_edge(u, v)
    return G


def generate_no_eulerian_path_multigraph(max_edges=14):
    G = nx.MultiGraph()
    nodes = list(range(0, random.randint(6, 10)))
    num_edges = random.randint(len(nodes) + 3, max_edges)
    edges = []
    for _ in range(num_edges):
        u, v = random.sample(nodes, 2)
        G.add_edge(u, v)
    G.add_edges_from(edges)

    while G.number_of_edges() < num_edges or has_eulerian_path(G):
        u, v = random.sample(nodes, 2)

        if random.random() < 0.1:
            u = len(nodes)

        G.add_edge(u, v)

        if random.random() < 0.5:
            u, v, k = random.sample(list(G.edges), 1)[0]
            G.remove_edge(u, v)

    return G


# Generate 10 such Eulerian MultiGraphs
correct_graphs = [generate_eulerian_path_multigraph() for _ in range(10)]

# Verify that each graph is Eulerian
for i, g in enumerate(correct_graphs):
    assert has_eulerian_path(g), f"Graph {i} has no Eulerian path"

wrong_graphs = [generate_no_eulerian_path_multigraph() for _ in range(20)]

# Verify each graph is non-Eulerian
for i, g in enumerate(wrong_graphs):
    assert not has_eulerian_path(g), f"Graph {i} has an Eulerian path!"


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
