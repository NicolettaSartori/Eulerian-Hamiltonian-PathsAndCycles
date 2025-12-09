import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from gviz import nx_to_graphviz, graphviz_to_svg_datauri, nx_to_graphviz_with_marked_path
from create_xml import format_list
from formatter_to_xml import clear_variable_declarations, format_to_xml
from functools import partial
import graphs
import generate_solutions as gs

def format_solutions(solutions):
    return format_list(
        [format_list(
            ["'" + item + "'" for item in solution]
        ) for solution in solutions]
    )
correct_paths = gs.find_all_eulerian_paths(graphs.new_graphs[0])


print(format_solutions(correct_paths))

