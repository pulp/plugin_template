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

PLUGIN_NAME="$(python ../plugin_template/scripts/get_template_config_value.py plugin_name)"
CI_UPDATE_DOCS="$(python ../plugin_template/scripts/get_template_config_value.py ci_update_docs)"
USE_BLACK="$(python ../plugin_template/scripts/get_template_config_value.py black)"

if [[ "${CI_UPDATE_DOCS}" == "True" ]]; then
  DOCS=("--docs")
else
  DOCS=()
fi

pushd ../plugin_template
  pip install -r requirements.txt
  ./plugin-template --github "${DOCS[@]}" "${PLUGIN_NAME}"
popd

if [[ $(git status --porcelain) ]]; then
  git add -A
  git commit -m "Update CI files"
else
  echo "No updates needed"
fi

if [[ "${USE_BLACK}" == "True" ]]
then
  pip install -r lint_requirements.txt
  black .

  if [[ "$(git status --porcelain)" ]]
  then
    git add -A
    git commit -m "Reformat with black"
  else
    echo "No formatting change needed"
  fi
fi

# Check that pulpcore lowerbounds is set to a supported branch
if [[ "${PLUGIN_NAME}" != "pulpcore" ]]; then
  python ../plugin_template/scripts/update_core_lowerbound.py
  if [[ $(git status --porcelain) ]]; then
    git add -A
    git commit -m "Bump pulpcore lowerbounds to supported branch"
  fi
fi
