import graphviz
import networkx as nx


def nx_to_graphviz(nx_graph, labeled_edges=False, labeled_nodes=True ):
    # g = graphviz.Graph(engine="neato", graph_attr={'mode': 'sgd', 'overlap': 'false', 'maxiter': '2000', 'splines': 'true'})

    g = graphviz.Graph(engine="neato", graph_attr={"overlap": "prism", "overlap_scaling": "-3", "splines": "true", "nodesep": "0.5"})

    g.attr("graph", center="True")

    for node in nx_graph.nodes():
        if labeled_nodes:
            g.node(str(node), label=chr(ord("A") + node - 1 ), shape="circle", fixedsize="true",
                 width="0.75", height="0.75")
        else:
            g.node(str(node), label="", shape="circle", fixedsize="true", width="0.75", height="0.75")

    idx = 0
    for edge in nx_graph.edges():
        if labeled_edges:
            g.edge(str(edge[0]), str(edge[1]), taillabel=chr(ord("a") + idx), labeldistance="1.5")
            idx += 1
        else:
            g.edge(str(edge[0]), str(edge[1]))

    return g


# G = nx.Graph([(1, 2), (2, 3), (3, 4), (4,1), (1,3)])
G = nx.Graph([(1, 2), (2, 3), (3, 4), (4,1),(1,5),(5,6),(6,7),(7,1 ),(3,1)])

# print(nx_to_graphviz(G,True, True).pipe(format="svg").decode("utf-8"))
# nx_to_graphviz(G).render('graph1', format='svg')
