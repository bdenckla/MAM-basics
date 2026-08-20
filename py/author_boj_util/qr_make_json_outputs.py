"""Generate JSON file with quirkrec field usage statistics."""

from collections import Counter
from mb_cmn.file_io import json_dump_to_file_path


def write_qr_field_stats_json(quirkrecs, out_path_by_count, out_path_by_name):
    """
    Write JSON files containing counts of all fields used in quirkrecs.

    Nested fields (dict values like qr-lc-loc) are reported as "parent.child"
    (e.g., "qr-lc-loc.page", "qr-lc-loc.column").

    Args:
        quirkrecs: List of quirkrec dicts (after processing, including nbd)
        out_path_by_count: Path to write the JSON file ordered by count
        out_path_by_name: Path to write the JSON file ordered by field name
    """
    field_counter = Counter()
    for qr in quirkrecs:
        for key, value in qr.items():
            field_counter[key] += 1
            # Handle nested dict fields (e.g., qr-lc-loc)
            if isinstance(value, dict):
                for nested_key in value:
                    field_counter[f"{key}.{nested_key}"] += 1

    # Sort by count descending, then by field name
    sorted_by_count = sorted(field_counter.items(), key=lambda x: (-x[1], x[0]))

    # Sort by field name
    sorted_by_name = sorted(field_counter.items(), key=lambda x: x[0])

    output_by_count = {
        "description": "Count of fields used in quirkrecs (ordered by count descending)",
        "total_quirkrecs": len(quirkrecs),
        "fields": [
            {"field": field, "count": count} for field, count in sorted_by_count
        ],
    }

    output_by_name = {
        "description": "Count of fields used in quirkrecs (ordered by field name)",
        "total_quirkrecs": len(quirkrecs),
        "fields": [{"field": field, "count": count} for field, count in sorted_by_name],
    }

    json_dump_to_file_path(output_by_count, out_path_by_count)
    json_dump_to_file_path(output_by_name, out_path_by_name)


def write_enriched_quirkrecs_json(quirkrecs, out_path):
    """
    Write a JSON file containing all quirkrecs data.

    Args:
        quirkrecs: List of quirkrec dicts (after processing, including nbd)
        out_path: Path to write the JSON file
    """
    json_dump_to_file_path(quirkrecs, out_path)


def write_qr_relations_json(qr_relations, out_path):
    """
    Write the authored cross-record relations to a JSON file.

    This is the relation-centric view (the per-record edges live on each
    quirkrec's qr-rel field in enriched-quirkrecs.json); it is provided for
    consumers that prefer to iterate relations directly.

    Args:
        qr_relations: the QR_RELATIONS list from qr_relations.py
        out_path: Path to write the JSON file
    """
    json_dump_to_file_path(qr_relations, out_path)
