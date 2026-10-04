"""Convert Semgrep crypto-rule findings into a CycloneDX 1.6 CBOM.

Each Semgrep rule in .github/semgrep/crypto-rules.yml carries a `cbom` metadata
block describing the cryptographic asset it detects. This script groups
matches by that asset (via `bomRef`) and emits one cryptographic-asset
component per asset, with one evidence occurrence per match location.
"""

import argparse
import json
import sys
import uuid
from datetime import UTC, datetime


def build_crypto_properties(cbom_meta: dict) -> dict:
    asset_type = cbom_meta["assetType"]
    properties: dict = {"assetType": asset_type}

    if asset_type == "algorithm":
        algorithm_properties = {"primitive": cbom_meta["primitive"]}
        if "mode" in cbom_meta:
            algorithm_properties["mode"] = cbom_meta["mode"]
        if "padding" in cbom_meta:
            algorithm_properties["padding"] = cbom_meta["padding"]
        if "cryptoFunctions" in cbom_meta:
            algorithm_properties["cryptoFunctions"] = cbom_meta["cryptoFunctions"]
        properties["algorithmProperties"] = algorithm_properties
    elif asset_type == "related-material":
        material_properties = {"type": cbom_meta.get("materialType", "other")}
        if "size" in cbom_meta:
            material_properties["size"] = cbom_meta["size"]
        properties["relatedCryptoMaterialProperties"] = material_properties

    return properties


def group_findings(results: list[dict]) -> dict[str, dict]:
    assets: dict[str, dict] = {}

    for result in results:
        cbom_meta = result.get("extra", {}).get("metadata", {}).get("cbom")
        if not cbom_meta:
            continue

        bom_ref = cbom_meta["bomRef"]
        path = result["path"]
        line = result["start"]["line"]

        asset = assets.setdefault(
            bom_ref,
            {
                "bom-ref": bom_ref,
                "name": cbom_meta["name"],
                "cbom_meta": cbom_meta,
                "occurrences": [],
            },
        )
        asset["occurrences"].append({"location": path, "line": line})

    return assets


def build_cbom(assets: dict[str, dict], repo_name: str, repo_version: str) -> dict:
    components = []
    depends_on = []

    for asset in sorted(assets.values(), key=lambda a: a["bom-ref"]):
        component = {
            "bom-ref": asset["bom-ref"],
            "type": "cryptographic-asset",
            "name": asset["name"],
            "cryptoProperties": build_crypto_properties(asset["cbom_meta"]),
            "evidence": {"occurrences": asset["occurrences"]},
        }
        if asset["cbom_meta"].get("weak"):
            component["properties"] = [
                {
                    "name": "cbom:weak",
                    "value": "Algorithm is cryptographically weak or deprecated.",
                }
            ]
        components.append(component)
        depends_on.append(asset["bom-ref"])

    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tools": [
                {"vendor": "Semgrep", "name": "semgrep", "version": "cli"},
                {
                    "vendor": repo_name,
                    "name": "semgrep_to_cbom.py",
                    "version": "1.0.0",
                },
            ],
            "component": {
                "bom-ref": repo_name,
                "type": "application",
                "name": repo_name,
                "version": repo_version,
            },
        },
        "components": components,
        "dependencies": [{"ref": repo_name, "dependsOn": depends_on}],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Semgrep JSON results file")
    parser.add_argument("--output", required=True, help="Output CBOM file path")
    parser.add_argument("--repo-name", required=True)
    parser.add_argument("--repo-version", default="0.0.0")
    args = parser.parse_args()

    with open(args.input) as f:
        semgrep_output = json.load(f)

    assets = group_findings(semgrep_output.get("results", []))
    cbom = build_cbom(assets, args.repo_name, args.repo_version)

    with open(args.output, "w") as f:
        json.dump(cbom, f, indent=2)
        f.write("\n")

    component_count = len(cbom["components"])
    print(f"Wrote {component_count} cryptographic-asset component(s) to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
