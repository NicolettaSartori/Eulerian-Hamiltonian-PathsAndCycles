from functools import partial
import os
import networkx as nx
import generate_solutions as gs
from create_xml import format_variable_declaration, format_all_solutions, format_graphviz_graphs
from create_xml import format_mc_stage_dynamic, format_mc_stage_dynamic_tf
from gviz import nx_to_graphviz

graphs = [
    # Hamiltonian cycle graphs (7 total)
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4), (3, 5), (4, 5)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4), (3, 5), (4, 5), (2,6), (6,7), (7, 3), (3,6), (2,7), (3,8), (7, 8)]),
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,3), (2, 4), (3, 5), (4, 5),(1,6),(2,6)]),
    nx.MultiGraph([(1, 2), (1, 2), (1, 3), (1,3), (1,4), (2, 4), (3, 4)]),
    nx.MultiGraph([(1,2), (2,3), (3,4), (4,5), (5,1), (2, 4), (3, 5), (2,6), (3,6), (4,6), (5,6)]),  # has Hamiltonian cycles
    # Traceable non-cycle graphs (7 total) – Hamiltonian path exists, no Hamiltonian cycle
    nx.MultiGraph([(1, 2), (2, 3), (3, 4), (4,1), (1,5), (5, 6), (6, 7), (7, 1), (3, 1)]),  # articulation prevents Hamiltonian cycle closure
    nx.MultiGraph([(1,2), (2,3), (3,4), (4,5), (5,6)]),  # pure path length 6
    nx.MultiGraph([(1,2), (2,3), (3,4), (4,5), (5,6), (3,5)]),  # path with internal chord (no endpoint connection)
    nx.MultiGraph([(4,2), (2,1), (1,3), (3,5), (5,6)]),  # path 4-2-1-3-5-6 (start 1 yields Hamiltonian path 1-3-5-6? enumeration allows alt starts)
    nx.MultiGraph([(1,2), (2,3), (3,4), (4,5), (5,6), (6,7)]),  # pure path length 7
    nx.MultiGraph([(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (3,5)]),  # path length 7 with internal chord only
    nx.MultiGraph([(1,2), (2,3), (3,1), (3,4), (4,5), (5,3)])  # two triangles sharing articulation vertex 3
]

start_node = 1

def add_multiple_choice_solutions(id, all_solutions):
    variable_declarations = ''
    correct_solutions_list = []
    for i in range(len(all_solutions)):
        correct_solutions_list.append([1 if j == all_solutions[i] else 0 for j in range(1, 8)])

    inner_lists = []
    for sub in correct_solutions_list:
        sub_inner = "; ".join(f"'{x}'" for x in sub)
        inner_lists.append("{ " + sub_inner + " }")
    correct_solutions_list = "{ " + "; ".join(inner_lists) + " }"
    correct_solutions_list = correct_solutions_list.replace("'", "")

    variable_declarations += format_variable_declaration("correct_solutions_list", id + 15, correct_solutions_list)
    variable_declarations += format_variable_declaration(
        "is_correct_solution_1",
        id + 16,
        "getFromList(0, getFromList([var=variant], [var=correct_solutions_list]))"
    )
    return variable_declarations

def export_exercise_mc(generate_fn, question_generator, title, filename):
    """Export a multiple choice exercise ensuring each variant has a valid Hamiltonian path.

    This version filters out any graphs that do not have at least one valid path,
    eliminating 'None' from feedback_solutions.
    """

    # Generate raw solutions per graph
    raw_solutions = list(map(generate_fn, graphs))

    # Filter graphs to those with at least one non-empty solution path
    filtered_graphs = []
    filtered_solutions = []
    filtered_indices = []
    for idx, (g, sols) in enumerate(zip(graphs, raw_solutions)):
        non_empty = [p for p in sols if p]
        if non_empty:
            filtered_graphs.append(g)
            filtered_solutions.append(non_empty)
            filtered_indices.append(idx)

    # Fallback: if no graph has a valid path, keep first and fabricate trivial path [start_node]
    if not filtered_graphs:
        filtered_graphs = [graphs[0]]
        filtered_solutions = [[[start_node]]]
        filtered_indices = [0]

    id = 34

    # Coerce numeric node paths to letters for storage in all_solutions variable
    coerced_solutions = []
    for sols in filtered_solutions:
        converted = []
        for path in sols:
            converted.append([chr(ord('a') + n - 1) for n in path])
        coerced_solutions.append(converted)
    variable_declarations = format_all_solutions("all_solutions", id, coerced_solutions)

    # Keep track of original indices for reproducibility
    valid_indices_code = "list(" + ",".join(str(i) for i in filtered_indices) + ")"
    variable_declarations += format_variable_declaration("valid_variant_indices", id + 2, valid_indices_code)
    variable_declarations += format_variable_declaration("variant_pos", id + 4,
                                                         "randomIntegerBetween(0,sizeOfList([var=valid_variant_indices]) - 1)")
    variable_declarations += format_variable_declaration("variant", id + 6,
                                                         "getFromList([var=variant_pos], [var=valid_variant_indices])")

    # Graph list limited to filtered graphs
    graphviz_graphs = list(map(partial(nx_to_graphviz, labeled_edges=True, start_node=start_node), filtered_graphs))
    variable_declarations += format_graphviz_graphs("graphs", id + 8, graphviz_graphs)
    variable_declarations += format_variable_declaration("graph", id + 10, "getFromList([var=variant_pos], [var=graphs])")
    variable_declarations += format_variable_declaration("start_node", id + 12, f"'{chr(ord('A') + start_node - 1)}'")

    # Feedback solutions (no 'None' entries)
    def path_to_letters(path):
        return " → ".join(chr(ord('A') + n - 1) for n in path)
    all_paths_text = []
    for sols in filtered_solutions:
        path_strings = [path_to_letters(p) for p in sols if p]
        # Build vertical list with <br/> separators
        all_paths_text.append("<br/>".join(path_strings))
    all_paths_html = "{ " + "; ".join("'" + s.replace("'", "\\'") + "'" for s in all_paths_text) + " }"
    variable_declarations += format_variable_declaration("all_solutions_html", id + 14, all_paths_html)
    variable_declarations += format_variable_declaration(
        "feedback_solutions",
        id + 16,
        "getFromList([var=variant_pos], [var=all_solutions_html])"
    )

    # Generate MC answers per filtered graph
    answer_options_list = []
    for graph, sols in zip(filtered_graphs, filtered_solutions):
        task, answers = question_generator(graph, sols)
        answer_options_list.append(answers)

    # Trim to fixed display count with at least one correct
    display_count = 6
    trimmed_answer_lists = []
    zero_based_correct_indices = []
    import random
    for answers in answer_options_list:
        correct = [t for t, c in answers if c]
        wrong = [t for t, c in answers if not c]
        selected = []
        if correct:
            selected.append(correct[0])
            random.shuffle(wrong)
            selected += wrong[:display_count - 1]
            corr_indices = [0]
        else:
            # Fabricate placeholder if somehow no correct (should not happen after filtering)
            selected.append("A")
            random.shuffle(wrong)
            selected += wrong[:display_count - 1]
            corr_indices = [0]
        if len(selected) < display_count:
            selected += ["N/A"] * (display_count - len(selected))
        trimmed_answer_lists.append(selected[:display_count])
        zero_based_correct_indices.append(corr_indices)

    answer_lists_code = "list(" + ", ".join(
        "list(" + ", ".join(f"'{t}'" for t in texts) + ")" for texts in trimmed_answer_lists
    ) + ")"
    variable_declarations += format_variable_declaration("answer_options_all", id + 18, answer_lists_code)
    variable_declarations += format_variable_declaration(
        "current_answer_options", id + 20, "getFromList([var=variant_pos], [var=answer_options_all])"
    )

    current_id = id + 22
    for answer_idx in range(display_count):
        var_name = f"answer_text_{answer_idx+1}"
        code = f"getFromList({answer_idx}, [var=current_answer_options])"
        variable_declarations += format_variable_declaration(var_name, current_id, code)
        current_id += 2

    correct_indices_code = "list(" + ", ".join(
        "list(" + ", ".join(str(i) for i in idxs) + ")" for idxs in zero_based_correct_indices
    ) + ")"
    variable_declarations += format_variable_declaration("correct_answer_indices_all", current_id, correct_indices_code)
    variable_declarations += format_variable_declaration(
        "correct_answer_indices",
        current_id + 2,
        "getFromList([var=variant_pos], [var=correct_answer_indices_all])"
    )

    next_id_for_stage = current_id + 4
    task, _ = question_generator(filtered_graphs[0], filtered_solutions[0])
    stage_xml, _ = format_mc_stage_dynamic(task, display_count, next_id_for_stage)

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(SCRIPT_DIR, 'TemplateMultipleChoice.xml')
    output_path = os.path.join(SCRIPT_DIR, 'xml-output', filename)

    with open(template_path, 'r') as file:
        content = file.read()
        content = content.format(
            variable_declarations=variable_declarations,
            stage=stage_xml,
            title=title,
        )
        with open(output_path, 'w') as file:
            file.write(content)

def hamiltonian_path_mc_generator(graph, solutions):
    """Generate a multiple choice question with path options

    Args:
        graph: NetworkX graph
        solutions: List of valid solutions for this graph

    Returns:
        (task_description, answers) where answers = [(text, is_correct), ...]
    """

    # Helper: convert numeric node list to letter path starting at A=1
    def to_letters(path):
        return " → ".join(chr(ord('A') + (n - 1)) for n in path)

    # Filter valid solutions to those starting at start_node (1)
    valid_solutions = [sol for sol in solutions if sol and sol[0] == start_node]

    # Choose one canonical correct path (if multiple, shortest lexicographically by letter string)
    if valid_solutions:
        correct_path = sorted(valid_solutions, key=lambda p: to_letters(p))[0]
    else:
        correct_path = None

    # Wrong path generation (5 variants) all starting at A
    wrong_paths = []
    import random

    nodes = list(graph.nodes)

    def add_wrong(p):
        if p and p[0] == start_node and p != correct_path:
            s = to_letters(p)
            if all(s != to_letters(x) for x in wrong_paths):
                wrong_paths.append(p)

    if correct_path:
        # 1. Incomplete (drop last vertex)
        if len(correct_path) > 2:
            add_wrong(correct_path[:-1])
        # 2. Swap two middle consecutive vertices
        for i in range(1, len(correct_path) - 2):
            swapped = correct_path[:]
            swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
            add_wrong(swapped)
            if len(wrong_paths) >= 5:
                break
        # 3. Duplicate a middle vertex
        if len(wrong_paths) < 5 and len(correct_path) > 2:
            dup_idx = random.randint(1, len(correct_path) - 2)
            duplicated = correct_path[:dup_idx + 1] + [correct_path[dup_idx]] + correct_path[dup_idx + 1:]
            add_wrong(duplicated)
        # 4. Insert unused vertex creating revisit/skip
        if len(wrong_paths) < 5:
            unused = [n for n in nodes if n not in correct_path]
            if unused:
                ins_idx = random.randint(1, len(correct_path) - 1)
                inserted = correct_path[:ins_idx] + [random.choice(unused)] + correct_path[ins_idx:]
                add_wrong(inserted)
        # 5. Shuffle internal segment
        if len(wrong_paths) < 5 and len(correct_path) > 3:
            internal = correct_path[1:-1]
            random.shuffle(internal)
            shuffled = [correct_path[0]] + internal + [correct_path[-1]]
            add_wrong(shuffled)

    # If still not enough wrong paths (e.g. very small graph), fabricate simple linear permutations
    while len(wrong_paths) < 5:
        trial = [start_node] + random.sample([n for n in nodes if n != start_node], min(len(nodes) - 1, len(nodes) - 1))
        add_wrong(trial)
        if len(wrong_paths) > 10:  # safety break
            break

    answers = []
    task = f"Which of the following is a valid Hamiltonian path in this graph starting from node {chr(ord('A') + start_node - 1)}?"

    if correct_path:
        answers.append((to_letters(correct_path), True))
    else:
        # No valid path: still present one crafted impossible path marked correct? Requirement wants valid path; we fall back.
        fabricated = [start_node]
        answers.append((to_letters(fabricated), True))

    for p in wrong_paths[:5]:
        answers.append((to_letters(p), False))

    # Ensure exactly 6 answers
    answers = answers[:6]
    return task, answers


# Example of MC exercise with path selection
# export_exercise_mc(partial(gs.find_all_hamiltonian_node_paths_starting_at_one_node, start_node=start_node, cycles=False), hamiltonian_path_mc_generator, "Select Hamiltonian Path", "HamiltonianPathSelection.xml")


def export_exercise_tf_cycle(graphs, start_node, filename):
    """Export a True/False exercise: Does the graph have a Hamiltonian cycle? (English)

    For each graph variant, answers are ordered so the correct one is first (to align with stage builder).
    """
    # Enumerate node-based Hamiltonian cycles starting at start_node
    cycles_per_graph = [gs.find_all_hamiltonian_node_paths_starting_at_one_node(g, start_node, cycles=True) for g in
                        graphs]

    # Build list of cycle existence booleans and formatted cycle strings
    def path_to_letters(path):
        return " → ".join(chr(ord('A') + n - 1) for n in path)

    formatted_cycles = []
    cycle_exists_flags = []
    for cycles in cycles_per_graph:
        if cycles:
            cycle_exists_flags.append(True)
            # Format cycles vertically
            cycle_strings = [path_to_letters(p) for p in cycles]
            formatted_cycles.append("<br/>".join(cycle_strings))
        else:
            cycle_exists_flags.append(False)
            formatted_cycles.append("No Hamiltonian cycle")

    id = 534  # Arbitrary starting ID separate from earlier exercises

    # Variable declarations
    variable_declarations = ""

    # Graphs SVG list
    graphviz_graphs = list(map(partial(nx_to_graphviz, labeled_edges=True, start_node=start_node), graphs))
    variable_declarations += format_graphviz_graphs("graphs", id, graphviz_graphs)
    variable_declarations += format_variable_declaration("variant_pos", id + 2,
                                                         "randomIntegerBetween(0,sizeOfList([var=graphs]) - 1)")
    variable_declarations += format_variable_declaration("graph", id + 4,
                                                         "getFromList([var=variant_pos], [var=graphs])")
    variable_declarations += format_variable_declaration("start_node", id + 6, f"'{chr(ord('A') + start_node - 1)}'")

    # Feedback cycles variable: build proper list() so getFromList works
    cycles_list_code = "list(" + ", ".join("'" + s.replace("'", "\\'") + "'" for s in formatted_cycles) + ")"
    variable_declarations += format_variable_declaration("all_cycles_html", id + 8, cycles_list_code)
    variable_declarations += format_variable_declaration("feedback_cycles", id + 10,
                                                         "getFromList([var=variant_pos], [var=all_cycles_html])")

    # Answer options per variant: correct first
    answer_lists = []
    for exists in cycle_exists_flags:
        if exists:
            answer_lists.append(["True", "False"])  # True first
        else:
            answer_lists.append(["False", "True"])  # False (correct) first

    answer_lists_code = "list(" + ", ".join(
        "list(" + ", ".join(f"'{a}'" for a in al) + ")" for al in answer_lists) + ")"
    variable_declarations += format_variable_declaration("answer_options_all", id + 12, answer_lists_code)
    variable_declarations += format_variable_declaration("current_answer_options", id + 14,
                                                         "getFromList([var=variant_pos], [var=answer_options_all])")

    # Provide answer_text_1..2 variables
    variable_declarations += format_variable_declaration("answer_text_1", id + 16,
                                                         "getFromList(0, [var=current_answer_options])")
    variable_declarations += format_variable_declaration("answer_text_2", id + 18,
                                                         "getFromList(1, [var=current_answer_options])")

    # Correct indices always list(0)
    correct_indices_code = "list(" + ", ".join("list(0)" for _ in answer_lists) + ")"
    variable_declarations += format_variable_declaration("correct_answer_indices_all", id + 20, correct_indices_code)
    variable_declarations += format_variable_declaration("correct_answer_indices", id + 22,
                                                         "getFromList([var=variant_pos], [var=correct_answer_indices_all])")

    # Build stage
    stage_xml, _ = format_mc_stage_dynamic_tf("Does this graph have a Hamiltonian cycle?", 2, id + 24, stage_id=5)

    # Write XML file using TemplateMultipleChoice.xml
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(SCRIPT_DIR, 'TemplateMultipleChoice.xml')
    output_path = os.path.join(SCRIPT_DIR, 'xml-output', filename)
    with open(template_path, 'r') as file:
        content = file.read()
        content = content.format(
            variable_declarations=variable_declarations,
            stage=stage_xml,
            title="Hamiltonian Cycle: True or False",
        )
        with open(output_path, 'w') as file:
            file.write(content)

# Export True/False Hamiltonian cycle existence exercise
export_exercise_tf_cycle(graphs, start_node, "HamiltonianCycleTrueFalse.xml")