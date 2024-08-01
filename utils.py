#!/usr/bin/env python3
import re
from pathlib import Path
from string import Template
from textwrap import dedent
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

    return [l.strip()[8:] for l in response.content.decode().split("\n") if "- name:" in l]


# Changelog to markdown migration

LEGACY_CHANGES_PLACEHOLDER_DATA = """\
Changes
*********

Removed due to docs migration process.
"""


def migrate_changelog_to_markdown(plugin_root: str, gh_org: str, gh_repo: str):
    """
    - Converts the changelog if there is a CHANGES.rst
    - Updates the pyproject.toml "tool.towncrier" section to use markdown if it doesnt.
    """
    root_path = Path(plugin_root)

    # pyproject update
    pyproject_file = root_path / "pyproject.toml"
    if (
        r'start_string = "[//]: # (towncrier release notes start)\n"'
        not in pyproject_file.read_text()
    ):
        update_pyproject_toml(pyproject_file, gh_org, gh_repo)

    # changelog conversion
    rst_changes = root_path / "CHANGES.rst"
    if rst_changes.exists():
        convert_changelog(rst_changes, gh_org, gh_repo)
        rst_changes.unlink()

    # manifest update
    manifest_file = root_path / "MANIFEST.in"
    if manifest_file.exists():
        manifest_updated = manifest_file.read_text().replace("CHANGES.rst", "CHANGES.md")
        manifest_file.write_text(manifest_updated)

    # docs/changes.rst fix
    legacy_changes_file = root_path / "docs" / "changes.rst"
    if legacy_changes_file.exists():
        legacy_changes_file.write_text(LEGACY_CHANGES_PLACEHOLDER_DATA)


def update_pyproject_toml(pyproject_file: Path, gh_org: str, gh_repo: str) -> Path:
    import tomlkit

    pyproject_data = tomlkit.loads(pyproject_file.read_text())

    TOWNCRIER_TOML_DATA = {
        "filename": "CHANGES.md",
        "directory": "CHANGES/",
        "title_format": "## {version} ({project_date}) {{: #{version} }}",
        "template": "CHANGES/.TEMPLATE.md",
        "issue_format": Template(
            "[#{issue}](https://github.com/$gh_org/$gh_repo/issues/{issue})"
        ).substitute(gh_org=gh_org, gh_repo=gh_repo),
        "start_string": "[//]: # (towncrier release notes start)\n",
        "underlines": ["", "", ""],
    }
    # update towncrier section
    for k, v in TOWNCRIER_TOML_DATA.items():
        pyproject_data["tool"]["towncrier"][k] = v  # type: ignore

    # re-write file
    pyproject_file.write_text(tomlkit.dumps(pyproject_data))
    return pyproject_file


def convert_changelog(changes_rst: Path, gh_org: str, gh_repo: str) -> Path:
    """Convert an rst changelog file to markdown.

    Args:
        changelog_file: The path to a rst changelog.
    Return:
        Path to new markdown changelog.
    """
    import pypandoc

    # pre-process
    cleaned = pre_process(changes_rst.read_text())
    changes_rst.write_text(cleaned)

    # convert
    changes_md = changes_rst.parent / "CHANGES.md"
    pypandoc.convert_file(
        source_file=str(changes_rst.absolute()),
        outputfile=str(changes_md.absolute()),
        to="markdown",
        extra_args=["--wrap=preserve"],
    )

    # pos-process
    cleaned = post_process(changes_md.read_text(), gh_org, gh_repo)
    changes_md.write_text(cleaned)
    return changes_md


def pre_process(document: str) -> str:
    replaces = [
        (
            "Convert :github: directive",
            r":github:`(\d+)`",
            r"`#\1 <https://github.com/%this_org_slash_repo%/issues/\1>`__",
        ),
        (
            "Convert :redmine: directive",
            r":redmine:`(\d+)`",
            r"`#\1 <https://pulp.plan.io/issues/\1>`__",
        ),
        (
            "Convert :ref: directive w/ <...>",
            r":ref:`([a-zA-Z_\s\.]+)\s<[a-zA-Z_\s\.]+>`",
            r"*\1*",
        ),
        (
            "Convert :meth: directive w/ <...>",
            r":meth:(`[a-zA-Z_\s\.]+`)",
            r"\1",
        ),
        (
            "Convert :ref: directive without <...>",
            r":ref:`([a-zA-Z_\s\.]+)`",
            r"*\1*",
        ),
    ]
    for _, pattern, repl in replaces:
        document = re.sub(pattern, repl, document)
    return document


def post_process(document: str, gh_org: str, gh_repo: str) -> str:
    replaces = [
        (
            "Remove # Changelog to include header later",
            r"#\sChangelog",
            "",
        ),
        (
            "Replace %this_org_slash_repo% with the plugin name",
            "%this_org_slash_repo%",
            f"{gh_org}/{gh_repo}",
        ),
        (
            "Use nice anchor links",  # x.y.z (YYYY-MM-DD) {: #x.y.z }
            r"## ([0-9]+\.[0-9]+\.[0-9]+) (\([0-9-]+\))",
            r"## \1 \2 {: #\1 }",
        ),
        (
            r"Remove backslahes before backticks",  # \' \* -> ' *
            r"\\(['\*`\"\[\]\<\>_~\-\.\$])",
            r"\1",
        ),
        (
            r"Remove []{.title-ref}",  # \' \* -> ' *
            r"\[([0-9a-zA-Z\_\s\.\-\/:\(\)\=]+)\]\{\.title-ref\}",
            r"\1",
        ),
        (
            r"Normalize dash separators",
            r"\n-+\n",
            "\n---\n",
        ),
        (
            "Remove double line breaks",
            r"^\n\n+",
            "",
        ),
    ]
    for _, pattern, repl in replaces:
        document = re.sub(pattern, repl, document)

    header = dedent(
        """\
        # Changelog

        [//]: # (You should *NOT* be adding new change log entries to this file, this)
        [//]: # (file is managed by towncrier. You *may* edit previous change logs to)
        [//]: # (fix problems like typo corrections or such.)
        [//]: # (To add a new change log entry, please see the contributing docs.)
        [//]: # (WARNING: Don't drop the towncrier directive!)

        [//]: # (towncrier release notes start)

        """
    )
    document = header + document
    return document
