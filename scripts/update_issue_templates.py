import sys

import yaml


def add_version(version: str, file: str) -> None:
    with open(file, "r", encoding='utf-8') as f:
        data = yaml.safe_load(f)
        for field in data["body"]:
            if field.get("id", "") == "package-version":
                field["attributes"]["options"] = [
                    version,
                    *field["attributes"]["options"],
                ]
    with open(file, "w+", encoding='utf-8') as f:
        yaml.dump(
            data, f, default_flow_style=False, sort_keys=False, allow_unicode=True
        )


def main() -> None:
    version = sys.argv[1]
    add_version(version, ".github/ISSUE_TEMPLATE/bug_report.yaml")
    add_version(version, ".github/ISSUE_TEMPLATE/issue.yaml")


if __name__ == "__main__":
    main()
