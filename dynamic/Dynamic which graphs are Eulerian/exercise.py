import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import networkx as nx
import random
from gviz import nx_to_graphviz, graphviz_to_svg_datauri
from create_xml import format_list
from formatter_to_xml import clear_variable_declarations, format_to_xml
from functools import partial


def generate_eulerian_multigraph(max_edges=12):
    G = nx.MultiGraph()
    nodes = list(range(1, random.randint(5, 8)))
    num_edges = random.randint(len(nodes) + 3, max_edges)
    #start with graph of random edges
    for _ in range(num_edges):
        u, v = random.sample(nodes, 2)        
        G.add_edge(u,v)
    
    # Remove random edge and add random edge until graph is eulerian
    while not nx.is_eulerian(G):
        u, v, k = random.choice(list(G.edges))
        G.remove_edge(u, v, k)
        u, v =random.sample(nodes, 2)
        G.add_edge(u, v)
    return G


def generate_non_eulerian_multigraph(max_edges=10):
    G = nx.MultiGraph()
    nodes = list(range(1, random.randint(5, 8)))
    num_edges = random.randint(len(nodes) + 1, max_edges)
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




wrong_feedbacks = [
   '"This graph is not Eulerian"' for _ in range(len(wrong_graphs))
]


correct_datauris = map(graphviz_to_svg_datauri, map(partial(nx_to_graphviz, labeled_edges=False), correct_graphs))
wrong_datauris = map(graphviz_to_svg_datauri, map(partial(nx_to_graphviz, labeled_edges=False), wrong_graphs))





exercise_constants = [
    ("correct_datauris", format_list(correct_datauris)),
    ("wrong_datauris", format_list(wrong_datauris)),
    ("wrong_feedbacks", format_list(wrong_feedbacks)),
    ("correct_index", "randomIntegerBetween(0, sizeOfList([var=correct_datauris]))"),
    ("correct_datauri", "getFromList([var=correct_index], [var=correct_datauris])"),
    ("num_wrong", "sizeOfList([var=wrong_datauris])"),
    ("wrong_indexes", 'evaluateInR("as.list(sample(1:[var=num_wrong], 3, replace = FALSE))")'),
    ("wrong_1_index", "getFromList(0, [var=wrong_indexes])"),
    ("wrong_2_index","getFromList(1, [var=wrong_indexes])"),
    ("wrong_3_index","getFromList(2, [var=wrong_indexes])"),
    ("wrong_1_datauri", "getFromList([var=wrong_1_index], [var=wrong_datauris])"),
    ("wrong_2_datauri","getFromList([var=wrong_2_index], [var=wrong_datauris])"),
    ("wrong_3_datauri","getFromList([var=wrong_3_index], [var=wrong_datauris])"),
    ("wrong_1_feedback","getFromList([var=wrong_1_index], [var=wrong_feedbacks])"),
    ("wrong_2_feedback","getFromList([var=wrong_2_index], [var=wrong_feedbacks])"),
    ("wrong_3_feedback","getFromList([var=wrong_3_index], [var=wrong_feedbacks])"),
    
]


clear_variable_declarations(".")

format_to_xml(".", [], 1, 1, exercise_constants)
