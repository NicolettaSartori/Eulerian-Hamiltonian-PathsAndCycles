from functools import partial
import os

import networkx as nx
import generate_solutions as gs
from create_xml import format_variable_declaration, format_all_solutions, format_graphviz_graphs
from create_xml import format_draggables
from formatter_html import format_list
from gviz import nx_to_graphviz

graphs = [
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4), (3, 5), (4, 5)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4), (3, 5), (4, 5), (2,6), (6,7), (7, 3), (3,6), (2,7), (3,8), (7, 8)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4), (3, 5), (4, 5),(1,6),(2,6)]),
    nx.MultiGraph([(1, 2), (1, 2), (1, 3), (1,3), (1,4), (2, 4), (3, 4)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,5), (5, 6), (6, 7), (7, 1), (3, 1)]),
    nx.MultiGraph([(1,2), (2,3), (3,4), (4,5), (5,1), (2, 4), (3, 5), (2,6), (3,6), (4,6), (5,6)]),
]

start_node = 1
# start_node = None

graphviz_graphs = map(partial(nx_to_graphviz, labeled_edges=True, start_node=start_node), graphs)

max_num_edges = max([len(g.edges) for g in graphs])


def export_exercise(generate_fn, title, article, type, filename):
    if start_node is not None:
        generate_fn = partial(gs.find_all_hamiltonian_cycles_starting_at_one_node, start_node=start_node)

    all_solutions = list(map(generate_fn, graphs))

    for solutions in all_solutions:
        if len(solutions) == 0:
            solutions.append([])

    id = 34

    variable_declarations = format_all_solutions("all_solutions", id, all_solutions)
    variable_declarations += format_variable_declaration("variant", id + 2,
                                                         "randomIntegerBetween(0,sizeOfList([var=all_solutions]) - 1)")
    variable_declarations += format_variable_declaration("active_solutions", id + 4,
                                                         "getFromList([var=variant], [var=all_solutions])")
    variable_declarations += format_graphviz_graphs("graphs", id + 6, graphviz_graphs)
    variable_declarations += format_variable_declaration("graph", id + 8, "getFromList([var=variant], [var=graphs])")
    variable_declarations += format_variable_declaration("start_node", id + 10, f"'{chr(ord('A') + start_node - 1)}'")

    all_solutions_html = [format_list(sols) for sols in all_solutions]
    all_solutions_html = "{ " + "; ".join(("'" + s.replace("'", "\\'") + "'") for s in all_solutions_html) + " }"
    variable_declarations += format_variable_declaration("all_solutions_html", id + 12, all_solutions_html)
    variable_declarations += format_variable_declaration(
        "feedback_solutions",
        id + 14,
        "getFromList([var=variant], [var=all_solutions_html])"
    )

    # Get the directory where this script is located
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    # Use absolute paths based on the script location
    template_path = os.path.join(SCRIPT_DIR, 'Template.xml')
    output_path = os.path.join(SCRIPT_DIR, 'xml-output', filename)

    with open(template_path, 'r') as file:
        content = file.read()
        # replace the placeholders in the template
        content = content.format(
            variable_declarations=variable_declarations,
            draggables=format_draggables("a", 27, max_num_edges),
            title=title,
            article=article,
            type=type,
        )
        with open(output_path, 'w') as file:
            file.write(content)


export_exercise(gs.find_all_eulerian_cycles_starting_at_one_node, "Find Eulerian Cycles","an", "eulerian cycle", "FindEulerianCycles.xml")
export_exercise(gs.find_all_eulerian_paths_starting_at_one_node, "Find Eulerian Paths", "an", "eulerian path", "FindEulerianPaths.xml")
export_exercise(gs.find_all_hamiltonian_cycles_starting_at_one_node, "Find Hamiltonian Cycles", "a", "hamiltonian cycle", "FindHamiltonianCycles.xml")
export_exercise(gs.find_all_hamiltonian_paths_starting_at_one_node, "Find Hamiltonian Paths", "a", "hamiltonian path", "FindHamiltonianPaths.xml")
