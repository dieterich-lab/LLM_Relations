"""
BRAT annotation parsing utilities.
"""

from pathlib import Path


def parse_brat_annotations(ann_file_path, text):
    """Parse BRAT format annotations and return structured entity information."""
    entities = []

    try:
        with open(ann_file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or not line.startswith("T"):
                    continue

                # Parse BRAT annotation line: T1\tEntityType start end\tentity_text
                parts = line.split("\t")
                if len(parts) != 3:
                    continue

                entity_id = parts[0]
                type_and_positions = parts[1].split()
                entity_text = parts[2]

                if len(type_and_positions) < 3:
                    continue

                entity_type = type_and_positions[0]
                try:
                    start_pos = int(type_and_positions[1])
                    end_pos = int(type_and_positions[2])
                except (ValueError, IndexError):
                    continue

                entity_info = {
                    "id": entity_id,
                    "type": entity_type,
                    "text": entity_text,
                    "start": start_pos,
                    "end": end_pos,
                }

                entities.append(entity_info)

    except FileNotFoundError:
        print(f"BRAT annotation file not found: {ann_file_path}")
    except Exception as e:
        print(f"Error parsing BRAT annotations: {e}")

    return entities
