from copy import deepcopy
import networkx as nx

# G = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1)])
# G = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3)])
# G = nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1),(1,5),(5,6),(6,7),(7,1 ),(3,1)])

G = nx.MultiGraph([(1, 2), (1, 2), (1, 3), (1, 3), (1, 4), (2, 4), (3, 4)])


def int_to_char(start, i):
    return chr(ord(start) + i)

def edges_to_chars(graph, edges):
    char_edges = []
    for edge in edges:
        # We don't know in which order the graph saves the nodes in the edge
        if edge not in list(graph.edges):
            edge = (edge[1], edge[0], edge[2])

        char_edges.append(int_to_char("a", list(graph.edges).index(edge)))

    return char_edges

def parallel_edge_keys(graph, u, v):
    for key in range(len(graph)):
        if graph.has_edge(u, v, key):
            yield key

def find_eulerian_paths(graph, node_path, edge_path, unused_edges, solutions, only_cycles=False):
    if len(unused_edges.edges) == 0:
        if not only_cycles or node_path[0] == node_path[-1]:
            solutions.append(edges_to_chars(graph, edge_path))
        return

    current_node = node_path[-1]
    neighbors = graph.neighbors(current_node)
    for neighbor in neighbors:
        if unused_edges.has_edge(current_node, neighbor):
            for key in parallel_edge_keys(unused_edges, current_node, neighbor):
                node_path.append(neighbor)
                edge_path.append((current_node, neighbor, key))
                unused_edges.remove_edge(current_node, neighbor, key)
                find_eulerian_paths(graph, node_path, edge_path, unused_edges, solutions, only_cycles)
                unused_edges.add_edge(current_node, neighbor, key)
                node_path.pop()
                edge_path.pop()



def find_hamiltonian_paths(graph, node_path, edge_path, unused_nodes, unused_edges, solutions, cycles=False):
    if cycles and len(unused_nodes) == 0:
        if node_path[0] == node_path[-1]:
            solutions.append(edges_to_chars(graph, edge_path))
            return
    elif not cycles and len(unused_nodes) == 1 and node_path[0] == unused_nodes[0]:
        solutions.append(edges_to_chars(graph, edge_path))
        return

    current_node = node_path[-1]
    neighbors = graph.neighbors(current_node)
    for neighbor in neighbors:
        if neighbor in unused_nodes and unused_edges.has_edge(current_node, neighbor):
            for key in parallel_edge_keys(unused_edges, current_node, neighbor):
                node_path.append(neighbor)
                edge_path.append((current_node, neighbor, key))
                new_unused_edges = deepcopy(unused_edges)
                new_unused_edges.remove_edge(current_node, neighbor, key)
                unused_nodes.remove(neighbor)
                find_hamiltonian_paths(graph, node_path, edge_path, unused_nodes, new_unused_edges, solutions, cycles)
                unused_nodes.append(neighbor)
                node_path.pop()
                edge_path.pop()



def two_odd_degree_nodes(graph):
    return sum([degree[1] % 2 for degree in graph.degree()]) == 2

def find_all_eulerian_cycles(graph):
    solutions = []
    if nx.is_eulerian(graph):
        for node in graph.nodes:
            unused_edges = deepcopy(graph)
            find_eulerian_paths(graph, [node], [], unused_edges, solutions, True)
    return solutions

def find_all_eulerian_cycles_starting_at_one_node(graph, start_node):
    solutions = []
    if nx.is_eulerian(graph):
        unused_edges = deepcopy(graph)
        find_eulerian_paths(graph, [start_node], [], unused_edges, solutions, True)
    return solutions

def find_all_eulerian_paths(graph):
    solutions = []
    if nx.is_eulerian(graph) or two_odd_degree_nodes(graph):
        for node in graph.nodes:
            unused_edges = deepcopy(graph)
            find_eulerian_paths(graph, [node], [], unused_edges, solutions)
    return solutions

def find_all_eulerian_non_cycle_paths(graph):
    solutions = []
    if two_odd_degree_nodes(graph):
        for node in graph.nodes:
            if (graph.degree(node) % 2 == 1):
                unused_edges = deepcopy(graph)
                find_eulerian_paths(graph, [node], [], unused_edges, solutions)
    return solutions

def find_all_eulerian_paths_starting_at_one_node(graph):
    if nx.is_eulerian(graph):
        return find_all_eulerian_cycles_starting_at_one_node(graph)
    if two_odd_degree_nodes(graph):
        return find_all_eulerian_non_cycle_paths(graph)
    return []

def find_all_hamiltonian_cycles(graph):
    solutions = []
    for node in graph.nodes:
        unused_edges = deepcopy(graph)
        find_hamiltonian_paths(graph, [node], [], list(graph.nodes), unused_edges, solutions, True)
    return solutions

def find_all_hamiltonian_cycles_starting_at_one_node(graph, start_node):
    solutions = []
    unused_edges = deepcopy(graph)
    find_hamiltonian_paths(graph, [start_node], [], list(graph.nodes), unused_edges, solutions, True)
    return solutions

def find_all_hamiltonian_paths(graph):
    solutions = []
    for node in graph.nodes:
        unused_edges = deepcopy(graph)
        find_hamiltonian_paths(graph, [node], [], list(graph.nodes), unused_edges, solutions)
    return solutions

def find_all_hamiltonian_paths_starting_at_one_node(graph, start_node):
    solutions = []
    for node in graph.nodes:
        unused_edges = deepcopy(graph)
        find_hamiltonian_paths(graph, [node], [], list(graph.nodes), unused_edges, solutions)
        if len(solutions) > 0: break
    return solutions
