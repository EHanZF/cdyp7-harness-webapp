from typing import Any, Dict, List


def validate_graph(graph: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []

    if not isinstance(graph, dict):
        return {"valid": False, "errors": ["Graph must be a dictionary"]}

    node_ids: set[str] = set()

    # Validate nodes
    nodes = graph.get("nodes")
    if nodes is None:
        errors.append("Missing 'nodes'")
    elif not isinstance(nodes, list):
        errors.append("'nodes' must be a list")
    else:
        for i, node in enumerate(nodes):
            if not isinstance(node, dict):
                errors.append(f"Node {i} must be an object")
                continue

            node_id = node.get("id")
            if not isinstance(node_id, str):
                errors.append(f"Node {i} must have a string 'id'")
            else:
                node_ids.add(node_id)

    # Validate edges
    edges = graph.get("edges")
    if edges is None:
        errors.append("Missing 'edges'")
    elif not isinstance(edges, list):
        errors.append("'edges' must be a list")
    else:
        for i, edge in enumerate(edges):
            if not isinstance(edge, dict):
                errors.append(f"Edge {i} must be an object")
                continue

            source = edge.get("source")
            target = edge.get("target")

            if not isinstance(source, str):
                errors.append(f"Edge {i} invalid 'source'")
            elif source not in node_ids:
                errors.append(f"Edge {i} source '{source}' not found")

            if not isinstance(target, str):
                errors.append(f"Edge {i} invalid 'target'")
            elif target not in node_ids:
                errors.append(f"Edge {i} target '{target}' not found")

    result: Dict[str, Any] = {
        "valid": len(errors) == 0,
        "errors": errors,
    }

    return result
