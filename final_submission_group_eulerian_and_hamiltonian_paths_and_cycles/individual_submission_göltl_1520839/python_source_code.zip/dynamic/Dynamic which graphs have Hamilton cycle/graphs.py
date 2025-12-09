import itertools

import networkx as nx


def find_hamiltonian_cycle(g):
    if len(g) == 0:
        return None
    for p in itertools.permutations(list(g.nodes)[1:]):
        # check if the cycle described by p is closed
        cycle = (0,) + p + (0,)
        valid_cycle = True
        i = 0
        while valid_cycle and i < len(cycle)-1:
            if not g.has_edge(cycle[i], cycle[i + 1]):
                valid_cycle = False
            i += 1
        # check whether cycle found
        if valid_cycle:
            return cycle
    return None

correct_graphs = [
    nx.from_graph6_bytes(g6)
    for g6 in
    [
        rb"Gs@ipo",
        rb"H@GSY^o",
        rb"Es\o",
        rb"G`_gqK",
        rb"G}hPW{",
        rb"F`o~_",
        rb"GsP@xw",
        rb"IA?HcPfnW",
        rb"G@hRSk"
    ]
]


correct_cycles = [find_hamiltonian_cycle(g) for g in correct_graphs]

wrong_graphs = [
    nx.from_graph6_bytes(g6)
    for g6 in
    [
        b"H?aFbx{",
        b"FIQ|o",
        b"F?~v_",
        b"FCS~?",
        b"FwC^w",
        b"DF{",
        b"F?~vw",
        b"GwC^?{",
        b"G_?ytK",
        b"I?_aCwuU_",
        b"G?G^]w",
        b"F?luW",
        b"F_G^w",
        b"G_?|Qs",
        b"FBFLW",
        b"F?ur_",
        b"GoCAh[",
        b"GGAXu[",
        b"G?O|fo",
        b"G`?Lz{",
        b"H??Kz^{"
    ]
]

def enquote_list(l):
    return ['"' + str + '"' for str in l]

wrong_feedbacks = enquote_list(["No, this graph doesn't have a Hamilton cycle" for _ in wrong_graphs])

if __name__ == "__main__":
    for i, g in enumerate(correct_graphs):
        assert find_hamiltonian_cycle(g), f"No hamilton cycle in graph {i + 1}"

    for i, g in enumerate(wrong_graphs):
        cycle = find_hamiltonian_cycle(g)
        assert not cycle, f"Hamilton cycle in graph {i+1}: {cycle}"
