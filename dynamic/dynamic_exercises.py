from functools import partial

import networkx as nx
import create_xml
import generate_solutions as gs
from create_xml import format_variable_declaration, format_all_solutions, format_graphviz_graphs
from create_xml import format_draggables, node_to_edge_solutions
from gviz import nx_to_graphviz

graphs = [
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4), (3, 5), (4, 5)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4), (3, 5), (4, 5), (2,6), (6,7), (7, 3), (3,6), (2,7), (3,8), (7, 8)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4), (3, 5), (4, 5),(1,6),(2,6)]),
    nx.MultiGraph([(1, 2), (1, 2), (1, 3), (1,3), (1,4), (2, 4), (3, 4)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,5), (5, 6), (6, 7), (7, 1), (3, 1)]),
    nx.MultiGraph([(1, 2), (1, 3), (1, 4), (1, 6), (1, 6), (2, 4), (2, 5), (2, 6), (2, 6), (3, 4), (3, 6), (3, 6), (4, 5), (4, 6), (5, 6), (5, 6)]),
    nx.MultiGraph([(1,2), (2,3), (3,4), (4,5), (5,1), (2, 4), (3, 5), (2,6), (3,6), (4,6), (5,6)]),
]

graphviz_graphs = map(partial(nx_to_graphviz, labeled_edges=True), graphs)

max_num_edges = max([len(g.edges) for g in graphs])


def export_exercise(generate_fn, article, type, filename):
    all_solutions = list(map(generate_fn, graphs))

    for solutions in all_solutions:
        if len(solutions) == 0:
            solutions.append([])

    id = 34

    variable_declarations = format_all_solutions("all_solutions", id, all_solutions)
    variable_declarations += format_variable_declaration("variant", id + 2,
                                                         "randomIntegerBetween(0,sizeOfList([var=all_solutions]))")
    variable_declarations += format_variable_declaration("active_solutions", id + 4,
                                                         "getFromList([var=variant], [var=all_solutions])")
    variable_declarations += format_graphviz_graphs("graphs", id + 6, graphviz_graphs)
    variable_declarations += format_variable_declaration("graph", id + 8, "getFromList([var=variant], [var=graphs])")
    variable_declarations += format_variable_declaration("start_node", id + 10,
                                                         "try(getFromList(0,getFromList(0,[var=active_solutions])),'a'")

    with open('Template.xml', 'r') as file:
        content = file.read()
        content = content.format(variable_declarations=variable_declarations,
                                 draggables=format_draggables("a", 27, max_num_edges), article=article,
                                 type=type)
        with open(filename, 'w') as file:
            file.write(content)


export_exercise(gs.find_all_eulerian_cycles_starting_at_one_node, "an", "eulerian cycle", "Find+Eulerian+Cycles.xml")
export_exercise(gs.find_all_eulerian_paths_starting_at_one_node, "an", "eulerian path", "Find+Eulerian+Paths.xml")
export_exercise(gs.find_all_hamiltonian_cycles_starting_at_one_node, "a", "hamiltonian cycle", "Find+Hamiltonian+Cycles.xml")
export_exercise(gs.find_all_hamiltonian_paths_starting_at_one_node, "a", "hamiltonian path", "Find+Hamiltonian+Paths.xml")
