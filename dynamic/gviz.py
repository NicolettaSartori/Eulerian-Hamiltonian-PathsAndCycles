import graphviz
import urllib
import networkx as nx
import xml.etree.ElementTree as ET

def svg_to_data_uri(svg_string: str) -> str:
    svg_string = svg_string.replace('"', "'")
    svg_string = ' '.join(svg_string.split())
    encoded_svg = urllib.parse.quote(svg_string, safe='()/,:')
    data_uri = f"data:image/svg+xml,{encoded_svg}"
    return data_uri

def graphviz_to_svg_datauri(graph):
    svg = graph.pipe(format='svg').decode('utf-8')

    # Extract the raw SVG content starting from <svg
    svg = svg[svg.index('<svg'):]
    # Encode to data URI
    data_uri = '"' + svg_to_data_uri(svg) + '"'
    return data_uri
    

def nx_to_graphviz(nx_graph, labeled_edges=False, labeled_nodes=True, start_node=None):
    # g = graphviz.Graph(engine="neato", graph_attr={'mode': 'sgd', 'overlap': 'false', 'maxiter': '2000', 'splines': 'true'})

    g = graphviz.Graph(engine="neato", graph_attr={"overlap": "prism", "overlap_scaling": "-3", "splines": "true", "nodesep": "0.5"})

    g.attr("graph", center="True")

    for node in nx_graph.nodes():
        if labeled_nodes:
            if node == start_node:                  
                g.node(str(node), label=f"{chr(ord("A") + node)}\n(Start)", shape="circle", penwidth="4",
                fixedsize="true", width="0.75", height="0.75")
            else:
                g.node(str(node), label=chr(ord("A") + node ), shape="circle", fixedsize="true",
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

def nx_to_graphviz_node_degree(nx_graph, labeled_edges=False, colored=False):

    g = graphviz.Graph(engine="neato", graph_attr={"overlap": "prism", "overlap_scaling": "-3", "splines": "true", "nodesep": "0.5"})

    g.attr("graph", center="True")

    for node in nx_graph.nodes():
        if colored and nx_graph.degree[node] % 2 == 1:
            g.node(str(node), label=f"{nx_graph.degree[node]}", shape="circle",
            fixedsize="true", fillcolor="red", width="0.75", height="0.75")
        else:
            g.node(str(node), label=f"{nx_graph.degree[node]}", shape="circle",
            fixedsize="true", width="0.75", height="0.75")

    idx = 0
    for edge in nx_graph.edges():
        if labeled_edges:
            g.edge(str(edge[0]), str(edge[1]), taillabel=chr(ord("a") + idx), labeldistance="1.5")
            idx += 1
        else:
            g.edge(str(edge[0]), str(edge[1]))

    return g


def nx_to_graphviz_with_marked_path(nx_graph, path=[], labeled_edges=False, labeled_nodes=True, start_node=None  ):

    edge_path = nx.Graph()
    for i in range(0, len(path)):
        edge_path.add_edge(path[i], path[(i+1)%len(nx_graph.nodes())])

    g = graphviz.Graph(engine="neato", graph_attr={"overlap": "prism", "overlap_scaling": "-3", "splines": "true", "nodesep": "0.5"})

    g.attr("graph", center="True")

    for node in nx_graph.nodes():
        if labeled_nodes:
            if node == start_node:
                g.node(str(node), label=f"{chr(ord("A") + node )}\n(Start)", shape="circle", penwidth="4",
                       fixedsize="true", width="0.75", height="0.75")
            else:
                g.node(str(node), label=chr(ord("A") + node ), shape="circle", fixedsize="true",
                       width="0.75", height="0.75")
        else:
            g.node(str(node), label="", shape="circle", fixedsize="true", width="0.75", height="0.75")

    idx = 0

    for edge in nx_graph.edges():
        if edge in edge_path.edges():
            if labeled_edges:
                g.edge(str(edge[0]), str(edge[1]), color="blue", taillabel=chr(ord("a") + idx), labeldistance="1.5")
                idx += 1
            else:
                g.edge(str(edge[0]), str(edge[1]), color="blue")
        else:
            if labeled_edges:
                g.edge(str(edge[0]), str(edge[1]), taillabel=chr(ord("a") + idx), labeldistance="1.5")
                idx += 1
            else:
                g.edge(str(edge[0]), str(edge[1]))

    return g

