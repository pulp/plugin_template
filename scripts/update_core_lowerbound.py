#!/bin/env python

import requests
import tomlkit
import yaml
from packaging.requirements import Requirement
from packaging.version import Version


CORE_TEMPLATE_URL = "https://raw.githubusercontent.com/pulp/pulpcore/main/template_config.yml"


def scan_requirement(line: str, supported_versions: set[Version]) -> str | None:
    new_requirement = None
    try:
        requirement = Requirement(line)
    except ValueError:
        pass
    else:
        if requirement.name == "pulpcore":
            for spec in requirement.specifier:
                if spec.operator == ">=":
                    min_version = Version(spec.version)
                    if (
                        Version(f"{min_version.major}.{min_version.minor}")
                        not in supported_versions
                    ):
                        # Lowerbound is not a supported branch, modify to next lowest
                        valid_lowerbounds = list(requirement.specifier.filter(supported_versions))
                        if valid_lowerbounds:
                            new_min_branch = min(valid_lowerbounds)
                            new_min_version = f"{new_min_branch.major}.{new_min_branch.minor}.0"
                            print(f"Lower bounds updated to >={new_min_version}")
                            new_requirement = line.replace(spec.version, new_min_version)
                        elif min_version > max(supported_versions):
                            print("This requirement is newer than any (yet) supported branches.")
                        else:
                            print(
                                f"No supported lower bounds {supported_versions} can satisfy"
                                " requirement range {requirement.specifier}, this branch can no"
                                " longer be supported."
                            )
                            exit(1)
                    break
    return new_requirement


def scan_pyproject_toml(supported_versions: set[Version]) -> None:
    changed = False
    with open("pyproject.toml") as fp:
        pyproject = tomlkit.load(fp)
        requirements: list[str] = pyproject["project"]["dependencies"]
        for i, line in enumerate(requirements):
            new_requirement = scan_requirement(line, supported_versions)
            if new_requirement is not None:
                requirements[i] = new_requirement
                changed = True
    if changed:
        with open("pyproject.toml", "w") as fp:
            tomlkit.dump(pyproject, fp)


def scan_requirements_txt(supported_versions: set[Version]) -> None:
    changed = False
    with open("requirements.txt") as fp:
        lines = fp.readlines()
        for i, line in enumerate(lines):
            requirement, sep, comment = line.partition(" #")
            new_requirement = scan_requirement(requirement, supported_versions)
            if new_requirement is not None:
                lines[i] = new_requirement + sep + comment
                changed = True
    if changed:
        with open("requirements.txt", "w") as fp:
            fp.writelines(lines)


def main() -> None:
    request = requests.get(CORE_TEMPLATE_URL)
    if request.status_code != 200:
        print("Failed to find supported branches, not checking lower bounds")
        exit(0)

    core_template = yaml.safe_load(request.content)
    supported_versions = {Version(v) for v in core_template["supported_release_branches"]}
    try:
        scan_pyproject_toml(supported_versions)
    except Exception:
        scan_requirements_txt(supported_versions)


if __name__ == "__main__":
    main()
