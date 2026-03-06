#!/usr/bin/env python3
"""Extract MONDO hierarchy from mondo.json into a compact JSON file.

Input:  mondo.json (OBO Graph JSON-LD, ~99MB)
Output: mondo-hierarchy.json (~5MB)

Format:
{
  "n": { "<numericId>": {"l": "label", "s": ["synonym1", ...]}, ... },
  "e": [["<childId>", "<parentId>"], ...]
}
"""

import json
import sys
import os

MONDO_PREFIX = "http://purl.obolibrary.org/obo/MONDO_"


def extract_numeric_id(uri):
    """Extract numeric part from MONDO URI, e.g. '0008426'."""
    if uri.startswith(MONDO_PREFIX):
        return uri[len(MONDO_PREFIX):]
    return None


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "mondo.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "mondo-hierarchy.json"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {input_path}...")
    with open(input_path) as f:
        data = json.load(f)

    graph = data["graphs"][0]
    nodes_raw = graph["nodes"]
    edges_raw = graph["edges"]

    # Extract MONDO nodes (skip deprecated)
    nodes = {}
    deprecated_count = 0
    for n in nodes_raw:
        nid = extract_numeric_id(n.get("id", ""))
        if nid is None:
            continue
        meta = n.get("meta", {})
        if meta.get("deprecated", False):
            deprecated_count += 1
            continue

        label = n.get("lbl", "")
        entry = {"l": label}

        # Extract exact synonyms
        synonyms = []
        for syn in meta.get("synonyms", []):
            if syn.get("pred") == "hasExactSynonym":
                val = syn.get("val", "")
                if val and val != label:
                    synonyms.append(val)
        if synonyms:
            entry["s"] = synonyms

        nodes[nid] = entry

    # Extract MONDO-to-MONDO is_a edges
    edges = []
    for e in edges_raw:
        if e.get("pred") != "is_a":
            continue
        child_id = extract_numeric_id(e.get("sub", ""))
        parent_id = extract_numeric_id(e.get("obj", ""))
        if child_id and parent_id and child_id in nodes and parent_id in nodes:
            edges.append([child_id, parent_id])

    result = {"n": nodes, "e": edges}

    print(f"Nodes: {len(nodes)} (skipped {deprecated_count} deprecated)")
    print(f"Edges: {len(edges)}")

    print(f"Writing {output_path}...")
    with open(output_path, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Done. Output size: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
