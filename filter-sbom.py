import json
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Filters cyclonedx-bom json SBOMS by pipdeptree jsons for a specific package",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--sbom", type=str, help="SBOM json file", default="cyclonedx.json"
    )

    parser.add_argument(
        "--out",
        type=str,
        help="SBOM json output file",
        default="cyclonedx_filtered.json",
    )

    parser.add_argument(
        "--dependencies",
        type=str,
        help="pipdeptree json file",
        default="dependencies.json",
    )

    parser.add_argument(
        "--extend-dependencies",
        dest="extend_dependencies",
        default=False,
        action="store_true",
    )

    args = parser.parse_args()

    with open(args.sbom, "r") as f:
        sbom = json.load(f)

    with open(args.dependencies, "r") as f:
        dependencies = json.load(f)

    dependency_packages = set(
        [
            (dep["package"]["package_name"], dep["package"]["installed_version"])
            for dep in dependencies
        ]
    )

    depends_on = dict()
    for dep in dependencies:
        depends_on[
            (dep["package"]["package_name"], dep["package"]["installed_version"])
        ] = dep["dependencies"]

    components = sbom["components"]

    components_to_keep = []
    components_to_remove = []
    component_refs_to_keep = dict()
    for c in components:
        if (c["name"], c["version"]) in dependency_packages:
            components_to_keep.append(c)
            component_refs_to_keep[(c["name"], c["version"])] = c["bom-ref"]
        else:
            components_to_remove.append(c["bom-ref"])

    sbom["components"] = components_to_keep
    sbom["dependencies"] = list(
        filter(lambda d: d["ref"] not in components_to_remove, sbom["dependencies"])
    )

    if args.extend_dependencies:
        extended_dependencies = []
        for k, v in component_refs_to_keep.items():
            deps = depends_on[k]
            tmp = {
                "ref": v,
                "dependsOn": [
                    component_refs_to_keep[(d["package_name"], d["installed_version"])]
                    for d in deps
                ],
            }
            extended_dependencies.append(tmp)

        sbom["dependencies"] = extended_dependencies

    with open(args.out, "w") as f:
        json.dump(sbom, f)


if __name__ == "__main__":
    main()

