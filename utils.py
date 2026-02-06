from datetime import timedelta
from pathlib import Path
import re
import stat
import textwrap
import tomllib

import requests_cache
import tomlkit
import yaml

# Jinja tests and filters


def is_valid(name):
    """
    Check if specified name is compliant with requirements for it.

    The max length of the name is 16 characters. It seems reasonable to have this limitation
    because the plugin name is used for directory name on the file system and it is also used
    as a name of some Python objects, like class names, so it is expected to be relatively short.
    """
    return bool(re.match(r"^[a-z][0-9a-z_]{2,15}$", name))


def to_camel(name):
    """
    Convert plugin name from snake to camel case
    """
    return name.title().replace("_", "")


def to_caps(name):
    """
    Convert plugin name from snake to upper snake case
    """
    return name.upper()


def to_dash(name):
    """
    Convert plugin name from snake case to dash representation
    """
    return name.replace("_", "-")


def to_snake(name):
    """
    Convert plugin name from snake case to dash representation
    """
    return name.replace("-", "_")


def to_nice_yaml(data):
    """Implement a filter for Jinja 2 templates to render human readable YAML."""
    return yaml.dump(data, indent=2, allow_unicode=True, default_flow_style=False)


def from_yaml(data):
    """Jinja filter to convert yaml data into a variable."""
    return yaml.safe_load(data)


# Information gathering


def ci_update_branches(config):
    release_branches = set()
    release_branches.add(config["latest_release_branch"])
    release_branches.update(config["supported_release_branches"])

    return [config["plugin_default_branch"]] + sorted(
        [branch for branch in release_branches if branch is not None]
    )


def current_version(plugin_root_path):
    try:
        path = plugin_root_path / "pyproject.toml"
        pyproject_toml = tomllib.loads(path.read_text())
        try:
            current_version = pyproject_toml["project"]["version"]
        except Exception:
            current_version = pyproject_toml["tool"]["bumpversion"]["current_version"]
    except Exception:
        try:
            path = plugin_root_path / ".bumpversion.cfg"
            for line in path.read_text().splitlines():
                if line.startswith("current_version = "):
                    current_version = line[18:].strip()
                    break
        except Exception:
            current_version = "0.0.0.dev"
    return current_version


def black_version():
    PATTERN = re.compile(r"^black==(?P<version>.*)$")
    requirements_file = Path(__file__).parent / "requirements.txt"
    for line in requirements_file.read_text().splitlines():
        if match := PATTERN.fullmatch(line):
            return match.group("version")

    raise ValueError("'black' not found in 'requirements.txt'")


def get_pulpdocs_members(pulpdocs_branch="main") -> list[str]:
    """
    Get repositories which are members of the Pulp managed documentation.

    Raises if can't get the authoritative file.
    """
    session = requests_cache.CachedSession(".requests_cache", expire_after=timedelta(days=1))
    response = session.get(
        f"https://raw.githubusercontent.com/pulp/pulp-docs/{pulpdocs_branch}/mkdocs.yml"
    )
    if response.status_code != 200:
        raise ValueError(
            "There was an error getting 'repolist.yml' from from pulp-docs repository."
            "This mean we can't know if we should manage the doc-related workflows."
        )

    class IgnoreTags(yaml.SafeLoader):
        pass

    IgnoreTags.add_multi_constructor("tag", lambda *a, **kw: None)
    mkdocs_config = yaml.load(response.content.decode(), Loader=IgnoreTags)
    repository_members = set()
    try:
        found = False
        for plugin in mkdocs_config["plugins"]:
            if "PulpDocs" in plugin:
                found = True
                for component in plugin["PulpDocs"]["components"]:
                    repository = component["path"].split("/")[0]
                    repository_members.add(repository)
                break
        if not found:
            raise KeyError("PulpDocs plugin not found")
    except KeyError:
        EXPECTED = """
        plugins:
          - PulpDocs:
              components:
                - title: "Pulpcore"
                  path: "pulpcore"
                  git_url: "https://github.com/pulp/pulpcore"
                  kind: "Core"
                  rest_api: "core"
                - ...
        """
        raise ValueError(f"Expected mkdocs.yml with structure:\n{textwrap.dedent(EXPECTED)}")

    return list(repository_members)


# Utilities for templating


def template_to_file(template, plugin_root_path, relative_path, template_vars):
    """
    Render template with values from the config and write it to the target plugin directory.
    """

    destination_path = plugin_root_path / relative_path
    data = template.render(**template_vars)
    destination_path.write_text(data + "\n")

    if destination_path.suffix in [".sh", ".py"]:
        mode = (
            stat.S_IRUSR
            | stat.S_IWUSR
            | stat.S_IXUSR
            | stat.S_IRGRP
            | stat.S_IWGRP
            | stat.S_IXGRP
            | stat.S_IROTH
            | stat.S_IXOTH
        )
    else:
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH
    destination_path.chmod(mode)


def merge_toml(template, plugin_root_path, relative_path, template_vars):
    """
    Template a file of the form 'basename.toml.merge_key' and combine its content beneath
    'merge_key' with the actual 'basename.toml' file.
    """
    basename, merge_key = relative_path.split(".toml.", maxsplit=1)
    data = tomlkit.loads(template.render(**template_vars))
    if merge_key in data:
        path = plugin_root_path / f"{basename}.toml"
        old_toml = tomlkit.load(path.open())
        if merge_key not in old_toml:
            old_toml[merge_key] = data[merge_key]
        else:
            old_toml[merge_key].update(data[merge_key])
        output = tomlkit.dumps(old_toml)
        if output[-1] != "\n":
            output = output + "\n"
        path.write_text(output)
