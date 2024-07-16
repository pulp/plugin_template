import requests
from yaml import safe_load
from packaging.requirements import Requirement
from packaging.version import parse


core_template_url = "https://raw.githubusercontent.com/pulp/pulpcore/main/template_config.yml"


def main():
    request = requests.get(core_template_url)
    if request.status_code != 200:
        print("Failed to find supported branches, not checking lower bounds")
        exit(0)

    template = safe_load(request.content)
    versions = {parse(v) for v in template.get("supported_release_branches", [])}
    if versions:
        changed = False
        with open("requirements.txt") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                try:
                    requirement = Requirement(line.split("#")[0].strip())
                except ValueError:
                    pass
                else:
                    if requirement.name == "pulpcore":
                        for spec in requirement.specifier:
                            if spec.operator == ">=":
                                min_version = parse(spec.version)
                                if min_version not in versions:
                                    # Lowerbound is not a supported branch, modify to next lowest
                                    valid_lowerbounds = list(requirement.specifier.filter(versions))
                                    if valid_lowerbounds:
                                        new_min_version = min(valid_lowerbounds)
                                        print(f"Lower bounds updated to >={new_min_version}")
                                        lines[i] = line.replace(spec.version, str(new_min_version))
                                        changed = True
                                    else:
                                        print(
                                            "No supported lower bounds can satisfy requirement"
                                            " range, this branch can no longer be supported."
                                        )
                                        exit(1)
                                break
        if changed:
            with open("requirements.txt", "w") as f:
                f.writelines(lines)


if __name__ == "__main__":
    main()
