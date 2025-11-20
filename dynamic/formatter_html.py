
def format_list(solutions):
    if solutions == [[]]:
        return "Empty"

    li_items = []
    for sol in solutions:
        path_str = " → ".join(str(v) for v in sol)
        li_items.append(f"<li>{path_str}</li>")
    html = "<ul>" + "".join(li_items) + "</ul>"
    return html