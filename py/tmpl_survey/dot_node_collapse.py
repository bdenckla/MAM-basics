"""Helpers for collapsing template-survey graph nodes."""


def _pick_representative(
    members,
    preferred_representatives=None,
    prefer_shortest_representative=False,
):
    """Pick a deterministic representative for a collapsed node group.

    Selection order:
    1) first preferred representative that is present in members;
    2) shortest member name (ties broken lexicographically) when enabled;
    3) lexicographically first member.
    """
    if preferred_representatives:
        members_set = set(members)
        for preferred in preferred_representatives:
            if preferred in members_set:
                return preferred
    if prefer_shortest_representative:
        return min(members, key=lambda x: (len(x), x))
    return sorted(members)[0]


def apply_collapse_node_groups(
    edges,
    collapse_node_groups,
    preferred_representatives=None,
    prefer_shortest_representative=False,
):
    """Apply explicit named-node merges before structural collapsing."""
    if not collapse_node_groups:
        return edges, {}

    all_nodes = set()
    for caller, callee in edges:
        all_nodes.add(caller)
        all_nodes.add(callee)

    replacement_by_name = {}
    explicit_group_members = {}
    for group in collapse_node_groups:
        present = [name for name in group if name in all_nodes]
        if len(present) < 2:
            continue
        representative = _pick_representative(
            present,
            preferred_representatives=preferred_representatives,
            prefer_shortest_representative=prefer_shortest_representative,
        )
        for name in present:
            replacement_by_name[name] = representative
        explicit_group_members[representative] = sorted(set(present))

    if not replacement_by_name:
        return edges, {}

    remapped_edges = {}
    for (caller, callee), count in edges.items():
        remapped_edge = (
            replacement_by_name.get(caller, caller),
            replacement_by_name.get(callee, callee),
        )
        remapped_edges[remapped_edge] = remapped_edges.get(remapped_edge, 0) + count

    return remapped_edges, explicit_group_members


def expand_groups_with_explicit_members(groups, explicit_group_members):
    """Attach explicitly merged node names to final collapsed tooltip groups."""
    if not explicit_group_members:
        return groups

    expanded = {}
    for rep, members in groups.items():
        merged = set(members)
        for member in members:
            merged.update(explicit_group_members.get(member, ()))
        expanded[rep] = sorted(merged)
    return expanded


def collapse_equivalent_nodes(
    edges,
    column_letters,
    preferred_representatives=None,
    prefer_shortest_representative=False,
):
    """Collapse nodes with identical predecessor/successor sets.

    Two non-column nodes are equivalent when they have the same set of
    predecessors and the same set of successors (ignoring edge counts).
    Returns (new_edges, groups) where groups maps each representative node
    to the sorted list of original nodes it stands for.
    """
    predecessors = {}
    successors = {}
    all_nodes = set()
    for caller, callee in edges:
        all_nodes.add(caller)
        all_nodes.add(callee)
        successors.setdefault(caller, set()).add(callee)
        predecessors.setdefault(callee, set()).add(caller)
    for node in all_nodes:
        predecessors.setdefault(node, set())
        successors.setdefault(node, set())

    collapsible = all_nodes - set(column_letters)

    sig_to_nodes = {}
    for node in collapsible:
        sig = (frozenset(predecessors[node]), frozenset(successors[node]))
        sig_to_nodes.setdefault(sig, []).append(node)

    node_to_rep = {}
    groups = {}
    for members in sig_to_nodes.values():
        sorted_members = sorted(members)
        rep = _pick_representative(
            sorted_members,
            preferred_representatives=preferred_representatives,
            prefer_shortest_representative=prefer_shortest_representative,
        )
        for member in sorted_members:
            node_to_rep[member] = rep
        groups[rep] = sorted_members

    for col in set(column_letters) & all_nodes:
        node_to_rep[col] = col

    new_edges = {}
    for (caller, callee), count in edges.items():
        new_caller = node_to_rep[caller]
        new_callee = node_to_rep[callee]
        new_edge = (new_caller, new_callee)
        new_edges[new_edge] = new_edges.get(new_edge, 0) + count

    return new_edges, groups


def collapse_edges_for_output(
    edges,
    column_letters,
    collapse_node_groups=None,
    preferred_representatives=None,
    prefer_shortest_representative=False,
):
    """Collapse full-graph edges with optional explicit named-node merges."""
    remapped_edges, explicit_group_members = apply_collapse_node_groups(
        edges,
        collapse_node_groups,
        preferred_representatives=preferred_representatives,
        prefer_shortest_representative=prefer_shortest_representative,
    )
    collapsed_edges, groups = collapse_equivalent_nodes(
        remapped_edges,
        column_letters,
        preferred_representatives=preferred_representatives,
        prefer_shortest_representative=prefer_shortest_representative,
    )
    groups = expand_groups_with_explicit_members(groups, explicit_group_members)
    return collapsed_edges, groups
