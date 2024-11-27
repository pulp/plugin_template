from datetime import timedelta
import itertools
import re
import requests_cache
import stat
import tomlkit
import tomllib
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


def get_pulpdocs_members() -> list[str]:
    """
    Get repositories which are members of the Pulp managed documentation.

    Raises if can't get the authoritative file.
    """
    session = requests_cache.CachedSession(".requests_cache", expire_after=timedelta(days=1))
    response = session.get(
        "https://raw.githubusercontent.com/pulp/pulp-docs/main/src/pulp_docs/data/repolist.yml"
    )
    if response.status_code != 200:
        raise ValueError(
            "There was an error getting 'repolist.yml' from from pulp-docs repository."
            "This mean we can't know if we should manage the doc-related workflows."
        )

    repolist = yaml.safe_load(response.content.decode())
    return [
        repo["name"]
        for repo in itertools.chain(*repolist["repos"].values())
        if "subpackage_of" not in repo
    ]


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
        tomlkit.dump(old_toml, path.open("w"))
