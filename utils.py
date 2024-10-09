#!/usr/bin/env python3
import re
import requests


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
    response = requests.get(
        "https://raw.githubusercontent.com/pulp/pulp-docs/main/src/pulp_docs/data/repolist.yml"
    )
    if response.status_code != 200:
        raise ValueError(
            "There was an error getting 'repolist.yml' from from pulp-docs repository."
            "This mean we can't know if we should manage the doc-related workflows."
        )

    return [line.strip()[8:] for line in response.content.decode().split("\n") if "- name:" in line]


def fetch_latest_pog_tag():
    response = requests.get(
        "https://api.github.com/repos/pulp/pulp-openapi-generator/git/refs/tags"
    )
    tags = [item["ref"] for item in response.json()]
    matched_tags = sorted(
        [
            ((int(match.group(1)), int(match.group(2))), f"{match.group(1)}.{match.group(2)}")
            for match in (re.fullmatch(r"^refs/tags/(\d{8})\.(\d+)$", tag) for tag in tags)
            if match is not None
        ]
    )
    return matched_tags[-1][1]
