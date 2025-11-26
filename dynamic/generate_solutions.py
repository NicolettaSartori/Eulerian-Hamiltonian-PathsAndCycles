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

def _direction_allowed(u, v, directed_edges):
    """
    directed_edges: set of (u, v) pairs meaning 'u -> v is allowed; v -> u is forbidden'.

    Rules:
    - if neither (u, v) nor (v, u) in directed_edges: treat as undirected -> allowed
    - if (u, v) in directed_edges: u -> v allowed
    - if (v, u) in directed_edges but not (u, v): u -> v forbidden
    """
    if not directed_edges:
        # no constraints at all
        return True

    if (u, v) in directed_edges:
        return True

    if (v, u) in directed_edges:
        return False

    # unconstrained edge = undirected behaviour
    return True


def find_hamiltonian_paths_with_directed_edges(
    graph,
    node_path,
    edge_path,
    unused_nodes,
    unused_edges,
    solutions,
    directed_edges,
    cycles=False,
):
    # ---- End conditions ----
    if cycles and len(unused_nodes) == 0:
        # Hamiltonian cycle: all nodes used and path closes
        if node_path[0] == node_path[-1]:
            solutions.append(edges_to_chars(graph, edge_path))
        return

    elif (not cycles) and len(unused_nodes) == 1 and node_path[0] == unused_nodes[0]:
        # Hamiltonian path variant (if you ever use it)
        solutions.append(edges_to_chars(graph, edge_path))
        return

    current_node = node_path[-1]

    for neighbor in graph.neighbors(current_node):
        if neighbor in unused_nodes and unused_edges.has_edge(current_node, neighbor):

            # respect direction constraints
            if not _direction_allowed(current_node, neighbor, directed_edges):
                continue

            for key in parallel_edge_keys(unused_edges, current_node, neighbor):
                node_path.append(neighbor)
                edge_path.append((current_node, neighbor, key))

                new_unused_edges = deepcopy(unused_edges)
                # remove the used edge
                if isinstance(new_unused_edges, (nx.MultiGraph, nx.MultiDiGraph)):
                    new_unused_edges.remove_edge(current_node, neighbor, key)
                else:
                    new_unused_edges.remove_edge(current_node, neighbor)

                unused_nodes.remove(neighbor)

                find_hamiltonian_paths_with_directed_edges(
                    graph,
                    node_path,
                    edge_path,
                    unused_nodes,
                    new_unused_edges,
                    solutions,
                    directed_edges,
                    cycles,
                )

                # backtrack
                unused_nodes.append(neighbor)
                node_path.pop()
                edge_path.pop()


def find_all_hamiltonian_cycles_starting_at_one_node_with_directed_edges(
    graph,
    directed_edges,
    start_node,
):
    """
    graph: nx.Graph or nx.MultiGraph
    directed_edges: iterable of (u, v) pairs (u -> v allowed direction)
    start_node: starting vertex for the cycle search
    """
    solutions = []
    unused_edges = deepcopy(graph)

    # IMPORTANT: include *all* nodes, including start_node
    unused_nodes = list(graph.nodes())

    # Use a set for fast lookup
    directed_edge_set = set(directed_edges)

    find_hamiltonian_paths_with_directed_edges(
        graph=graph,
        node_path=[start_node],
        edge_path=[],
        unused_nodes=unused_nodes,
        unused_edges=unused_edges,
        solutions=solutions,
        directed_edges=directed_edge_set,
        cycles=True,
    )

    return solutions



def find_all_hamiltonian_paths(graph):
    solutions = []
    for node in graph.nodes:
        unused_edges = deepcopy(graph)
        find_hamiltonian_paths(graph, [node], [], list(graph.nodes), unused_edges, solutions)
    return solutions

def find_all_hamiltonian_paths_starting_at_one_node(graph, start_node, cycles=False):
    solutions = []
    unused_edges = deepcopy(graph)
    find_hamiltonian_paths(graph, [start_node], [], list(graph.nodes), unused_edges, solutions, cycles)
    return solutions

# Node-based Hamiltonian path enumeration (returns sequences of node indices instead of edge labels)
def _dfs_hamiltonian_nodes(graph, path, unused_nodes, solutions, cycles):
    if cycles and len(unused_nodes) == 0:
        if path[0] == path[-1]:
            solutions.append(path.copy())
        return
    elif not cycles and len(unused_nodes) == 1 and path[0] == unused_nodes[0]:
        solutions.append(path.copy())
        return

    current = path[-1]
    for neighbor in graph.neighbors(current):
        if neighbor in unused_nodes:
            path.append(neighbor)
            unused_nodes.remove(neighbor)
            _dfs_hamiltonian_nodes(graph, path, unused_nodes, solutions, cycles)
            unused_nodes.append(neighbor)
            path.pop()

def find_all_hamiltonian_node_paths_starting_at_one_node(graph, start_node, cycles=False):
    solutions = []
    _dfs_hamiltonian_nodes(graph, [start_node], list(graph.nodes), solutions, cycles)
    return solutions


def generate_wrong_paths(graph, valid_solutions, num_wrong=2):
    """Generate plausible but incorrect paths for multiple choice questions
    
    Args:
        graph: NetworkX graph
        valid_solutions: List of valid solutions (as lists of node indices)
        num_wrong: Number of wrong paths to generate
    
    Returns:
        List of wrong path solutions
    """
    wrong_paths = []
    nodes = list(graph.nodes)
    edges = list(graph.edges(keys=True))
    
    # Strategy 1: Remove the last node from valid solutions (incomplete paths)
    for solution in valid_solutions:
        if len(solution) > 2:
            incomplete_path = solution[:-1]
            if incomplete_path not in wrong_paths and incomplete_path not in valid_solutions:
                wrong_paths.append(incomplete_path)
                if len(wrong_paths) >= num_wrong:
                    return wrong_paths
    
    # Strategy 2: Swap two consecutive nodes
    for solution in valid_solutions:
        if len(solution) > 2:
            for i in range(len(solution) - 1):
                swapped = solution.copy()
                swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
                if swapped not in wrong_paths and swapped not in valid_solutions:
                    # Check if it's still a valid path (connected)
                    if all(graph.has_edge(swapped[j], swapped[j+1]) for j in range(len(swapped)-1)):
                        wrong_paths.append(swapped)
                        if len(wrong_paths) >= num_wrong:
                            return wrong_paths
    
    # Strategy 3: Add a random node in the middle
    for solution in valid_solutions:
        if len(solution) > 1:
            for i in range(1, len(solution)):
                for node in nodes:
                    if node not in solution:
                        modified = solution[:i] + [node] + solution[i:]
                        if modified not in wrong_paths and modified not in valid_solutions:
                            # Check connectivity
                            if all(graph.has_edge(modified[j], modified[j+1]) for j in range(len(modified)-1)):
                                wrong_paths.append(modified)
                                if len(wrong_paths) >= num_wrong:
                                    return wrong_paths
    
    # Strategy 4: Random valid-looking paths that start from the same node
    from random import choice, sample
    for _ in range(num_wrong * 2):
        if len(wrong_paths) >= num_wrong:
            break
        path = [nodes[0]]
        for _ in range(len(nodes) - 1):
            neighbors = [n for n in graph.neighbors(path[-1])]
            if neighbors:
                path.append(choice(neighbors))
            else:
                break
        if path not in wrong_paths and path not in valid_solutions:
            wrong_paths.append(path)
    
    return wrong_paths[:num_wrong]

def find_nodes_to_make_hamiltonian_cycle_impossible(graph, removed_nodes):
    n1, n2, n3 = removed_nodes

    # If the original graph already has no Hamiltonian cycle, return 0.
    if not find_all_hamiltonian_cycles(graph):
        return 0

    tests = [
        (1, [n1]),              # only first
        (2, [n2]),              # only second
        (3, [n3]),              # only third
        (4, [n1, n2]),          # first & second
        (5, [n1, n3]),          # first & third
        (6, [n2, n3]),          # second & third
        (7, [n1, n2, n3]),      # all three
    ]

    for code, nodes_to_remove in tests:
        g_reduced = graph.copy()
        g_reduced.remove_nodes_from(nodes_to_remove)

        # If there are no Hamiltonian cycles left after removing these nodes:
        if not find_all_hamiltonian_cycles(g_reduced):
            return code

    # If none of these removals kills all Hamiltonian cycles, return 0.
    return 0
