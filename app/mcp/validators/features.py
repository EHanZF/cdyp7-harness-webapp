# app/mcp/validators/features.py
import csv

def validate_features(file):
    rows = csv.DictReader(file.file.read().decode().splitlines())
    errors, warnings = [], []

    for i, r in enumerate(rows):
        if r["entropy_class"] == "High" and not r["synonyms"]:
            errors.append(f"Row {i}: High entropy feature missing synonyms")

        if r["platform"] != "S750":
            errors.append(f"Row {i}: Cross-platform contamination")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }
