#!/bin/env python3

# This script is running with elevated privileges from the main branch against pull requests.

import re
import sys
from pathlib import Path

import tomllib
from git import Repo

# Files that change the third-party CI image. Plugin app code is not listed; those PRs overlay
# the PR wheel on the nightly prebuilt deps image.
PLUGIN_DEP_PATHS = (
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "requirements.txt",
    "requirements.in",
    "ci_requirements.txt",
    ".ci/assets/ci_constraints.txt",
    ".ci/scripts/calc_constraints.py",
    "template_config.yml",
)

# plugin_template itself: anything that changes how the catdog image is built or locked.
TEMPLATE_DEP_PATHS = (
    "plugin-template",
    "templates/github/.ci/",
    "templates/github/.github/workflows/scripts/before_install.sh.j2",
)


def dep_prefixes() -> tuple[str, ...]:
    if Path("templates/github").is_dir() and Path("plugin-template").exists():
        return TEMPLATE_DEP_PATHS
    return PLUGIN_DEP_PATHS


def is_dep_path(path: str | None) -> bool:
    if not path:
        return False
    for prefix in dep_prefixes():
        if prefix.endswith("/"):
            if path.startswith(prefix) or path == prefix.rstrip("/"):
                return True
        elif path == prefix:
            return True
    return False


def changed_paths(repo: Repo, base_commit, head_commit) -> set[str]:
    paths: set[str] = set()
    for diff in base_commit.diff(head_commit):
        if diff.a_path:
            paths.add(diff.a_path)
        if diff.b_path:
            paths.add(diff.b_path)
    return paths


def deps_changed(repo: Repo, base_commit, head_commit) -> bool:
    return any(is_dep_path(path) for path in changed_paths(repo, base_commit, head_commit))


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--deps-changed":
        repo = Repo(".")
        base_commit = repo.commit(sys.argv[2])
        head_commit = repo.commit(sys.argv[3])
        print("1" if deps_changed(repo, base_commit, head_commit) else "0")
        return

    assert len(sys.argv) == 3

    with open("pyproject.toml", "rb") as fp:
        PYPROJECT_TOML = tomllib.load(fp)
    BLOCKING_REGEX = re.compile(r"DRAFT|WIP|NO\s*MERGE|DO\s*NOT\s*MERGE|EXPERIMENT")
    ISSUE_REGEX = re.compile(r"(?:fixes|closes)[\s:]+#(\d+)")
    CHERRY_PICK_REGEX = re.compile(r"^\s*\(cherry picked from commit [0-9a-f]*\)\s*$")
    try:
        CHANGELOG_EXTS = {
            f".{item['directory']}" for item in PYPROJECT_TOML["tool"]["towncrier"]["type"]
        }
    except KeyError:
        CHANGELOG_EXTS = {".feature", ".bugfix", ".doc", ".removal", ".misc"}

    repo = Repo(".")

    base_commit = repo.commit(sys.argv[1])
    head_commit = repo.commit(sys.argv[2])

    pr_commits = list(repo.iter_commits(f"{base_commit}..{head_commit}"))

    labels = {
        "multi-commit": len(pr_commits) > 1,
        "cherry-pick": False,
        "no-issue": False,
        "no-changelog": False,
        "wip": False,
        "no-cache": deps_changed(repo, base_commit, head_commit),
    }
    for commit in pr_commits:
        labels["wip"] |= BLOCKING_REGEX.search(commit.summary) is not None
        no_issue = ISSUE_REGEX.search(commit.message, re.IGNORECASE) is None
        labels["no-issue"] |= no_issue
        cherry_pick = CHERRY_PICK_REGEX.search(commit.message) is not None
        labels["cherry-pick"] |= cherry_pick
        changelog_snippets = [
            k
            for k in commit.stats.files
            if k.startswith("CHANGES/") and Path(k).suffix in CHANGELOG_EXTS
        ]
        labels["no-changelog"] |= not changelog_snippets

    print("ADD_LABELS=" + ",".join((k for k, v in labels.items() if v)))
    print("REMOVE_LABELS=" + ",".join((k for k, v in labels.items() if not v)))


if __name__ == "__main__":
    main()
