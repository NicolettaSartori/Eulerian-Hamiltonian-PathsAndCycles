import urllib.parse

import graphviz

def int_to_char(start, i):
    return chr(ord(start) + i)


def escape_html(s):
    return s.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def svg_to_data_uri(svg_string: str) -> str:
    # Replace double quotes with single quotes
    svg_string = svg_string.replace('"', "'")
    # Remove newlines and extra whitespace
    svg_string = ' '.join(svg_string.split())
    # Percent-encode special characters for use in URL
    encoded_svg = urllib.parse.quote(svg_string, safe='()/,\':')
    # Prepend the header for SVG data URIs
    data_uri = f"data:image/svg+xml,{encoded_svg}"
    return data_uri

def format_list(l):
    return "list(" + ",".join(l) + ")"

def format_variable_declaration(name, id, code):
    return """
    <VariableDeclaration id="{id1}">
      <name>{name}</name>
      <initializationCode id="{id2}">
        <code>{code}</code>
        <domain>MATH</domain>
      </initializationCode>
    </VariableDeclaration>
    """.format(id1=id, id2=id + 1, name=name, code=escape_html(code))


def format_graphviz_graph(graph):
    svg = graph.pipe(format='svg').decode('utf-8')
    svg = "\"<img src=" + svg_to_data_uri(svg[svg.index('<svg'):]) + ">\""
    # svg = svg[svg.index('<svg'):]
    return svg

def format_graphviz_graphs(name, id, graphs):
    return format_variable_declaration(name, id, format_list([format_graphviz_graph(graph) for graph in graphs]))

def format_solutions(solutions):
    return format_list(
        [format_list(
            ["&apos;" + item + "&apos;" for item in solution]
        ) for solution in solutions]
    )

def format_all_solutions(name, id, all_solutions):
    return format_variable_declaration(name, id, format_list([format_solutions(solutions) for solutions in all_solutions]))

def node_to_edge_solutions(solutions, edges):
    return [list(edges).index(edge) for edge in zip(solutions[0:-1], solutions[1:])]


def format_draggable(name, id):
    return '''<DNDVisibleZonesDraggable id="{id}">
    <variableName>{name}</variableName>
    <htmlContent>&lt;div&gt;{name}&lt;/div&gt;</htmlContent>
    <numberOfDraggables>1</numberOfDraggables>
    <infiniteDraggables>false</infiniteDraggables>
    <dndVisibleZonesStage reference="5"/>
</DNDVisibleZonesDraggable>
'''.format(name=name,id=id)

def format_draggables(start, id , num):
    string = ""
    for i in range(num):
        string += format_draggable(int_to_char(start, i), id)
        id += 1
    return string



