# cyclonedx-sbom-filter
Filters cyclonedx-py json files by pipdeptree json output

## Usage

1. Install your package and `cyclonedx-bom` and `pipdeptree` (preferably in a virtual environment)

```shell
$ pip install <package_name> cyclonedx-bom pipdeptree
```

2. Create SBOM and dependency file

```shell
# create SBOM of current virtual env
$ cyclonedx-py -pb --format json -e

# create pipdeptree file
$ pipdeptree -p <package_name> --json > dependencies.json
```

3. Filter SBOM
```shell
$ python filter-sbom.py --sbom cyclonedx.json --dependencies dependencies.json --out cyclonedx_filtered.json

# or also extend dependencies
$ python filter-sbom.py --sbom cyclonedx.json --dependencies dependencies.json --out cyclonedx_filtered.json --extend-dependencies
```
