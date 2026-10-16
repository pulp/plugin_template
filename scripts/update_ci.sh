#!/usr/bin/env bash

set -eu -o pipefail

if [ ! -f "template_config.yml" ]
then
  echo "No template_config.yml detected."
  exit 1
fi

if [ "${1:-}" = "--release" ]
then
  echo "Running on a release branch"

  sed -i \
    -e 's/^\(ci_update_docs: \)true$/\1false/' \
    -e 's/^\(docs_test: \)true$/\1false/' \
    "template_config.yml"
fi

if [[ $(git status --porcelain) ]]
then
  echo "Working directory not clean. Aborting."
  exit 1
fi

PLUGIN_NAME="$(uv run --script ../plugin_template/scripts/get_template_config_value.py plugin_name)"
CI_UPDATE_DOCS="$(uv run --script ../plugin_template/scripts/get_template_config_value.py ci_update_docs)"

if [[ "${CI_UPDATE_DOCS}" == "True" ]]; then
  DOCS=("--docs")
else
  DOCS=()
fi

uv run --script ../plugin_template/plugin-template --github "${DOCS[@]}"

if [[ $(git status --porcelain) ]]; then
  git add -A
  git commit -m "Update CI files"
else
  echo "No updates needed"
fi

# Check that pulpcore lowerbounds is set to a supported branch
if [[ "${PLUGIN_NAME}" != "pulpcore" ]]; then
  uv run --script ../plugin_template/scripts/update_core_lowerbound.py
  if [[ $(git status --porcelain) ]]; then
    git add -A
    git commit -m "Bump pulpcore lowerbounds to supported branch"
  fi
fi
