import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import networkx as nx
import random
from gviz import nx_to_graphviz, graphviz_to_svg_datauri, nx_to_graphviz_node_degree
from create_xml import format_list
from formatter_to_xml import clear_variable_declarations, format_to_xml
from functools import partial


def generate_eulerian_multigraph(max_edges=14):
    G = nx.MultiGraph()
    nodes = list(range(1, random.randint(6, 10)))
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


def generate_non_eulerian_multigraph(max_edges=14):
    G = nx.MultiGraph()
    nodes = list(range(1, random.randint(6, 10)))
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




# wrong_feedbacks = [
#    '"This graph is not Eulerian because not all node degrees are even.\n\n[va]"' for _ in range(len(wrong_graphs))
# ]


correct_graphviz = [nx_to_graphviz(g, labeled_nodes=False, labeled_edges=False) for g in correct_graphs]
correct_datauris = [graphviz_to_svg_datauri(gv) for gv in correct_graphviz]

wrong_graphviz = [nx_to_graphviz(g, labeled_nodes=False, labeled_edges=False) for g in wrong_graphs]
wrong_datauris = [graphviz_to_svg_datauri(gv) for gv in wrong_graphviz]

correct_with_degrees_graphviz = [nx_to_graphviz_node_degree(g, colored=True, labeled_edges=False) for g in correct_graphs]
correct_with_degrees_datauris = [graphviz_to_svg_datauri(gv) for gv in correct_with_degrees_graphviz]

wrong_with_degrees_graphviz = [nx_to_graphviz_node_degree(g, colored=True, labeled_edges=False) for g in wrong_graphs]
wrong_with_degrees_datauris = [graphviz_to_svg_datauri(gv) for gv in wrong_with_degrees_graphviz]





exercise_constants = [
    ("correct_datauris", format_list(correct_datauris)),
    ("wrong_datauris", format_list(wrong_datauris)),
    ("correct_with_degrees_datauris", format_list(correct_with_degrees_datauris)),
    ("wrong_with_degrees_datauris", format_list(wrong_with_degrees_datauris)),
    # ("wrong_feedbacks", format_list(wrong_feedbacks)),
    ("correct_index", "randomIntegerBetween(0, sizeOfList([var=correct_datauris]))"),
    ("correct_datauri", "getFromList([var=correct_index], [var=correct_datauris])"),
    ("correct_with_degrees_datauri", "getFromList([var=correct_index], [var=correct_with_degrees_datauris])"),
    ("num_wrong", "sizeOfList([var=wrong_datauris])"),
    ("wrong_indexes", 'evaluateInR("as.list(sample(0:([var=num_wrong]-1), 3, replace = FALSE))")'),
    ("wrong_1_index", "getFromList(0, [var=wrong_indexes])"),
    ("wrong_2_index","getFromList(1, [var=wrong_indexes])"),
    ("wrong_3_index","getFromList(2, [var=wrong_indexes])"),
    ("wrong_1_datauri", "getFromList([var=wrong_1_index], [var=wrong_datauris])"),
    ("wrong_2_datauri","getFromList([var=wrong_2_index], [var=wrong_datauris])"),
    ("wrong_3_datauri","getFromList([var=wrong_3_index], [var=wrong_datauris])"),
    # ("wrong_1_feedback","getFromList([var=wrong_1_index], [var=wrong_feedbacks])"),
    # ("wrong_2_feedback","getFromList([var=wrong_2_index], [var=wrong_feedbacks])"),
    # ("wrong_3_feedback","getFromList([var=wrong_3_index], [var=wrong_feedbacks])"),
    ("wrong_1_with_degrees_datauri","getFromList([var=wrong_1_index], [var=wrong_with_degrees_datauris])"),
    ("wrong_2_with_degrees_datauri","getFromList([var=wrong_2_index], [var=wrong_with_degrees_datauris])"),
    ("wrong_3_with_degrees_datauri","getFromList([var=wrong_3_index], [var=wrong_with_degrees_datauris])"),

    
]


clear_variable_declarations(".")

format_to_xml(".", [], 1, 1, exercise_constants)
