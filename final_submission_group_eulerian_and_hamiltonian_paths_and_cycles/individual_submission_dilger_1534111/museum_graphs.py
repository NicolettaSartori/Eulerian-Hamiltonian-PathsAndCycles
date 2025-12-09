import graphviz
import random
import itertools
import math
import urllib.parse

inf = math.inf
x = -inf

def has_hamiltonian_path(g):
    if len(g) == 0:
        return False, None
    n = len(g)
    for path in itertools.permutations(range(n)):
        valid = True
        i = 0
        while valid and i < len(path) - 1:
            if g[path[i]][path[i+1]] == x:
                valid = False
            i += 1
        if valid:
            return True, list(path)
    return False, None

def find_all_hamiltonian_paths(g):
    if len(g) == 0:
        return []
    n = len(g)
    all_paths = []
    for path in itertools.permutations(range(n)):
        valid = True
        i = 0
        while valid and i < len(path) - 1:
            if g[path[i]][path[i+1]] == x:
                valid = False
            i += 1
        if valid:
            all_paths.append(list(path))
    return all_paths

def generate_hamiltonian_graph(num_nodes=5, seed=None):
    if seed is not None:
        random.seed(seed)
    
    for attempt in range(100):
        base_path = list(range(num_nodes))
        random.shuffle(base_path)
        g = [[x for _ in range(num_nodes)] for _ in range(num_nodes)]
        
        for i in range(len(base_path) - 1):
            g[base_path[i]][base_path[i+1]] = 1
        
        for node in range(num_nodes):
            current = sum(1 for j in range(num_nodes) if g[node][j] != x)
            target = random.randint(2, 3)
            while current < target:
                t = random.randint(0, num_nodes - 1)
                if t != node and g[node][t] == x:
                    g[node][t] = 1
                    current += 1
        
        has_path, _ = has_hamiltonian_path(g)
        if has_path:
            return g
    raise ValueError("Failed to generate graph")

def graph_to_graphviz_svg(g, labels, exhibit_names):
    n = len(g)
    
    dot = graphviz.Digraph()
    dot.attr('graph', rankdir='LR', size='8,5')
    dot.format = 'svg'
    
    for i in range(n):
        if i == 0:
            dot.node(f'node_{i}', f'{exhibit_names[i]}\\n(Entrance)', 
                    shape="circle", penwidth="4",
                    fixedsize="true", width="0.75", height="0.75")
        else:
            dot.node(f'node_{i}', exhibit_names[i], 
                    shape="circle",
                    fixedsize="true", width="0.75", height="0.75")
    
    hallway_num = 1
    for i in range(n):
        for j in range(n):
            if g[i][j] != x:
                dot.edge(f'node_{i}', f'node_{j}', label=f'Hall {hallway_num}')
                hallway_num += 1

    svg_string = dot.pipe(format='svg').decode('utf-8')
    
    svg_encoded = urllib.parse.quote(svg_string, safe='')
    
    return f'<img src=data:image/svg+xml,{svg_encoded}>'


num_variants = 10
all_solutions = []
graphs = []
html_solutions = []

labels = ['A', 'B', 'C', 'D', 'E']

exhibit_names = ['Ancient\\nEgypt', 'Medieval\\nArmor', 'Modern\\nArt', 'Natural\\nHistory', 'Space\\nExhibit']

exhibit_full = ['Ancient Egypt', 'Medieval Armor', 'Modern Art', 'Natural History', 'Space Exhibit']

for i in range(num_variants):
    g = generate_hamiltonian_graph(5, seed=i*100)
    paths = find_all_hamiltonian_paths(g)
    
    paths_from_entrance = [path for path in paths if path[0] == 0]
    

    letter_paths = [[labels[idx] for idx in path] for path in paths_from_entrance]
    all_solutions.append(letter_paths)

    graphs.append(graph_to_graphviz_svg(g, labels, exhibit_names))
    
    html = '<ul>'
    for path in paths_from_entrance:
        route = ' → '.join([exhibit_full[idx] for idx in path])
        html += '<li>' + route + '</li>'
    html += '</ul>'
    html_solutions.append(html)

print("all_solutions:")
out = "list("
for variant in all_solutions:
    out += "list("
    for path in variant:
        out += "list(" + ",".join([f"'{c}'" for c in path]) + "),"
    out = out.rstrip(',') + "),"
out = out.rstrip(',') + ")"
print(out)

print("\n\ngraphs:")
out = "list("
for g in graphs:
    out += "'" + g + "',"
out = out.rstrip(',') + ")"
print(out)

print("\n\nall_solutions_html:")
out = "{"
for h in html_solutions:
    h_escaped = h.replace("'", "\\'")
    out += "'" + h_escaped + "';"
out = out.rstrip(';') + "}"
print(out)