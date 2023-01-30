import re

from tomlkit import loads

Version = tuple[str, str, str, str, str]


def main() -> None:
    with open("pyproject.toml", "r", encoding="utf-8") as f:
        pyproject = loads(f.read())
    current_version: str = pyproject["tool"]["poetry"]["version"]  # type:ignore
    print(  # noqa:T201,T001
        version_to_str(next_beta_version(parse_version(version=current_version)))
    )


def parse_version(version: str) -> Version:
    pattern = re.compile(
        r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"  # noqa:E501 # pylint:disable=line-too-long
    )
    match = pattern.search(version)
    if not match:
        raise ValueError(f"{version} is not a version")

    return tuple(n and str(n) or "" for n in match.groups(0))  # type:ignore


def next_beta_version(version: Version) -> Version:
    major, minor, patch, prerelease, buildmetadata = version
    if not prerelease:
        return major, minor, patch, prerelease, buildmetadata
    prerelease_n = int(prerelease.removeprefix("beta"))
    return (major, minor, patch, "beta" + str(prerelease_n + 1), buildmetadata)


def version_to_str(version: Version) -> str:
    major, minor, patch, prerelease, _ = version
    return f"{major}.{minor}.{patch}-{prerelease}"


if __name__ == "__main__":
    main()
