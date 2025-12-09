import graphs
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from gviz import nx_to_graphviz

for i, g in enumerate(graphs.correct_graphs):

    nx_to_graphviz(g).render(f"graphs/correct_{i+1}", format='pdf', cleanup=True)

for i, g in enumerate(graphs.wrong_graphs):
    nx_to_graphviz(g).render(f"graphs/wrong_{i+1}", format='pdf', cleanup=True)
