#!/bin/env python

import requests
import tomlkit
import yaml
from packaging.requirements import Requirement
from packaging.version import parse


core_template_url = "https://raw.githubusercontent.com/pulp/pulpcore/main/template_config.yml"


def scan_requirement(line, supported_versions):
    updated = False
    new_requirement = None
    try:
        requirement = Requirement(line)
    except ValueError:
        pass
    else:
        if requirement.name == "pulpcore":
            for spec in requirement.specifier:
                if spec.operator == ">=":
                    min_version = parse(spec.version)
                    if parse(f"{min_version.major}.{min_version.minor}") not in supported_versions:
                        # Lowerbound is not a supported branch, modify to next lowest
                        valid_lowerbounds = list(requirement.specifier.filter(supported_versions))
                        if valid_lowerbounds:
                            new_min_branch = min(valid_lowerbounds)
                            new_min_version = f"{new_min_branch.major}.{new_min_branch.minor}.0"
                            print(f"Lower bounds updated to >={new_min_version}")
                            new_requirement = line.replace(spec.version, new_min_version)
                            updated = True
                        else:
                            print(supported_versions)
                            print(
                                "No supported lower bounds can satisfy requirement"
                                " range, this branch can no longer be supported."
                            )
                            exit(1)
                    break
    return updated, new_requirement


def scan_pyproject_toml(supported_versions):
    changed = False
    with open("pyproject.toml") as fp:
        pyproject = tomlkit.load(fp)
        requirements = pyproject["project"]["dependencies"]
        for i, line in enumerate(requirements):
            updated, new_requirement = scan_requirement(line, supported_versions)
            if updated:
                requirements[i] = new_requirement
                changed = True
    if changed:
        with open("pyproject.toml", "w") as fp:
            tomlkit.dump(pyproject, fp)


def scan_requirements_txt(supported_versions):
    changed = False
    with open("requirements.txt") as fp:
        lines = fp.readlines()
        for i, line in enumerate(lines):
            requirement, sep, comment = line.partition(" #")
            updated, new_requirement = scan_requirement(requirement, supported_versions)
            if updated:
                lines[i] = new_requirement + sep + comment
                changed = True
    if changed:
        with open("requirements.txt", "w") as fp:
            fp.writelines(lines)


def main():
    request = requests.get(core_template_url)
    if request.status_code != 200:
        print("Failed to find supported branches, not checking lower bounds")
        exit(0)

    core_template = yaml.safe_load(request.content)
    supported_versions = {parse(v) for v in core_template["supported_release_branches"]}
    latest = core_template["latest_release_branch"]
    supported_versions.add(parse(latest))
    try:
        scan_pyproject_toml(supported_versions)
    except Exception:
        scan_requirements_txt(supported_versions)


if __name__ == "__main__":
    main()
