from datetime import timedelta
import itertools
import pathlib
import re
import requests_cache
import tomllib
import yaml


def current_version(plugin_root_dir):
    plugin_root_dir = pathlib.Path(plugin_root_dir)
    try:
        path = plugin_root_dir / "pyproject.toml"
        pyproject_toml = tomllib.loads(path.read_text())
        current_version = pyproject_toml["project"]["version"]
    except Exception:
        try:
            path = plugin_root_dir / ".bumpversion.cfg"
            for line in path.read_text().splitlines():
                if line.startswith("current_version = "):
                    current_version = line[18:].strip()
                    break
        except Exception:
            current_version = "0.1.0a1.dev"
    return current_version


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
