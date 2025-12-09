import graphs
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import gviz
from gviz import nx_to_graphviz

for i, g in enumerate(graphs.old_graphs):
    nx_to_graphviz(g).render(f"graphs/old_{i+1}", format="svg", cleanup=True)

for i, g in enumerate(graphs.new_graphs):
    nx_to_graphviz(g).render(f"graphs/new_{i+1}", format='svg', cleanup=True)

nx_to_graphviz(graphs.old_graphs[0],True, center_lables=True).render(f"graphs/old_correct_labled", format='svg', cleanup=True)
gviz.nx_to_graphviz_with_marked_path(graphs.old_graphs[0],[0,1,2,3,0]).render(f"graphs/old_correct_labled_hamilton_cycle", format='svg', cleanup=True)
gviz.nx_to_graphviz_with_marked_path(graphs.old_graphs[0],[0,1,2,3]).render(f"graphs/old_correct_labled_hamilton_path", format='svg', cleanup=True)
gviz.nx_to_graphviz_node_degree(graphs.old_graphs[0]).render(f"graphs/old_correct_node_degrees", format='svg', cleanup=True)

nx_to_graphviz(graphs.new_graphs[0],True, center_lables=True).render(f"graphs/new_correct_labled", format='svg', cleanup=True)
gviz.nx_to_graphviz_node_degree(graphs.new_graphs[0]).render(f"graphs/new_correct_node_degrees", format='svg', cleanup=True)
gviz.nx_to_graphviz_with_marked_path(graphs.new_graphs[0],[0,1,2,3,0]).render(f"graphs/new_correct_labled_hamilton_cycle", format='svg', cleanup=True)
gviz.nx_to_graphviz_with_marked_path(graphs.new_graphs[0],[0,1,2,3]).render(f"graphs/new_correct_labled_hamilton_path", format='svg', cleanup=True)
