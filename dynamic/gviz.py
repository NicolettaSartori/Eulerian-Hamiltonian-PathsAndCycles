import graphviz
import urllib
import networkx as nx

def svg_to_data_uri(svg_string: str) -> str:
    svg_string = svg_string.replace('"', "'")
    svg_string = ' '.join(svg_string.split())
    encoded_svg = urllib.parse.quote(svg_string, safe='()/,\':')
    data_uri = f"data:image/svg+xml,{encoded_svg}"
    return data_uri

def graphviz_to_svg_datauri(graph):
    svg = graph.pipe(format='svg').decode('utf-8')
    svg = '"' + svg_to_data_uri(svg[svg.index('<svg'):]) + '"'
    return svg

def nx_to_graphviz(nx_graph, labeled_edges=False, labeled_nodes=True, start_node=0  ):
    # g = graphviz.Graph(engine="neato", graph_attr={'mode': 'sgd', 'overlap': 'false', 'maxiter': '2000', 'splines': 'true'})

    g = graphviz.Graph(engine="neato", graph_attr={"overlap": "prism", "overlap_scaling": "-3", "splines": "true", "nodesep": "0.5"})

    g.attr("graph", center="True")

    for node in nx_graph.nodes():
        if labeled_nodes:
            if node == start_node:                  
                dot.node(str(node), label=f"{chr(odr("A") + node - 1)}\n(Start)", shape="circle", penwidth="4",
                fixedsize="true", width="0.75", height="0.75")
            else:
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


