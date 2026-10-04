"""Render a CycloneDX CBOM (cryptographic-asset components) as Markdown.

Works on either a hand-authored CBOM (richer fields: oid, security levels,
related-material sizes) or the leaner CBOM produced by semgrep_to_cbom.py,
since every field is read defensively with .get().
"""

import argparse
import json
import os
import sys
from datetime import UTC, datetime

WEAK_PROPERTY_NAMES = {"cbom:weak", "cbom:risk", "cbom:quantum-safety"}


def resolve_under_cwd(path: str) -> str:
    """Resolve `path` and reject it if it escapes the working directory."""
    base_dir = os.path.realpath(os.getcwd())
    resolved = os.path.realpath(path)
    if os.path.commonpath([base_dir, resolved]) != base_dir:
        raise ValueError(f"Path '{path}' resolves outside the working directory")
    return resolved


def crypto_components(cbom: dict) -> list[dict]:
    return [
        c for c in cbom.get("components", []) if c.get("type") == "cryptographic-asset"
    ]


def asset_type(component: dict) -> str:
    return component.get("cryptoProperties", {}).get("assetType", "unknown")


def format_occurrences(component: dict) -> str:
    occurrences = component.get("evidence", {}).get("occurrences", [])
    if not occurrences:
        return "_no location recorded_"
    lines = sorted(
        {f"`{o['location']}:{o['line']}`" for o in occurrences if "line" in o}
    )
    return ", ".join(lines) if lines else "_no location recorded_"


def format_algorithm_row(component: dict) -> str:
    props = component.get("cryptoProperties", {})
    alg = props.get("algorithmProperties", {})
    name = component.get("name", "?")
    primitive = alg.get("primitive", "-")
    detail_parts = []
    if "mode" in alg:
        detail_parts.append(f"mode={alg['mode']}")
    if "padding" in alg:
        detail_parts.append(f"padding={alg['padding']}")
    if alg.get("parameterSetIdentifier"):
        detail_parts.append(f"params={alg['parameterSetIdentifier']}")
    detail = ", ".join(detail_parts) if detail_parts else "-"
    functions = ", ".join(alg.get("cryptoFunctions", [])) or "-"
    locations = format_occurrences(component)
    return f"| {name} | {primitive} | {detail} | {functions} | {locations} |"


def format_protocol_row(component: dict) -> str:
    name = component.get("name", "?")
    locations = format_occurrences(component)
    return f"| {name} | {locations} |"


def format_material_row(component: dict) -> str:
    props = component.get("cryptoProperties", {})
    material = props.get("relatedCryptoMaterialProperties", {})
    name = component.get("name", "?")
    material_type = material.get("type", "-")
    size = material.get("size")
    size_str = f"{size} bits" if size else "-"
    locations = format_occurrences(component)
    return f"| {name} | {material_type} | {size_str} | {locations} |"


def collect_risk_notes(component: dict) -> list[str]:
    notes = []
    for prop in component.get("properties", []):
        if prop.get("name") in WEAK_PROPERTY_NAMES:
            notes.append(f"**{component.get('name', '?')}** — {prop['value']}")
    return notes


def render(cbom: dict, project_name: str, generated: str) -> str:
    components = crypto_components(cbom)
    algorithms = [c for c in components if asset_type(c) == "algorithm"]
    protocols = [c for c in components if asset_type(c) == "protocol"]
    materials = [c for c in components if asset_type(c) == "related-material"]
    risk_notes = [note for c in components for note in collect_risk_notes(c)]

    spec_version = cbom.get("specVersion", "?")
    lines = [
        "# Cryptography Bill of Materials (CBOM)",
        "",
        f"**Project:** {project_name}  ",
        f"**Format:** CycloneDX {spec_version} (machine-readable: CBOM.json)  ",
        f"**Generated:** {generated}  ",
        f"**Status:** {len(components)} cryptographic asset(s) identified  ",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Category | Count |",
        "|---|---|",
        f"| Algorithms | {len(algorithms)} |",
        f"| Protocols | {len(protocols)} |",
        f"| Related material (keys, IVs, salts) | {len(materials)} |",
        f"| Flagged risks | {len(risk_notes)} |",
        "",
        "---",
        "",
    ]

    if algorithms:
        lines += [
            "## Algorithms",
            "",
            "| Name | Primitive | Detail | Functions | Found at |",
            "|---|---|---|---|---|",
        ]
        lines += [
            format_algorithm_row(c) for c in sorted(algorithms, key=lambda c: c["name"])
        ]
        lines += ["", "---", ""]

    if protocols:
        lines += [
            "## Protocols",
            "",
            "| Name | Found at |",
            "|---|---|",
        ]
        lines += [
            format_protocol_row(c) for c in sorted(protocols, key=lambda c: c["name"])
        ]
        lines += ["", "---", ""]

    if materials:
        lines += [
            "## Related Cryptographic Material",
            "",
            "| Name | Type | Size | Found at |",
            "|---|---|---|---|",
        ]
        lines += [
            format_material_row(c) for c in sorted(materials, key=lambda c: c["name"])
        ]
        lines += ["", "---", ""]

    lines += ["## Flagged Risks", ""]
    if risk_notes:
        lines += [f"- {note}" for note in risk_notes]
    else:
        lines += ["No weak or deprecated cryptographic assets were flagged."]
    lines += ["", "---", ""]

    lines += [
        "## References",
        "",
        "- [CycloneDX CBOM Specification](https://cyclonedx.org/capabilities/cbom/)",
        "- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)",
        "",
    ]

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CBOM JSON file (CycloneDX)")
    parser.add_argument("--output", required=True, help="Output Markdown file path")
    parser.add_argument("--project-name", required=True)
    args = parser.parse_args()

    with open(args.input) as f:
        cbom = json.load(f)

    generated = cbom.get("metadata", {}).get("timestamp") or datetime.now(UTC).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    markdown = render(cbom, args.project_name, generated)

    output_path = resolve_under_cwd(args.output)
    with open(output_path, "w") as f:
        f.write(markdown)

    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
