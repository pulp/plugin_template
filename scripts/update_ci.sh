#!/usr/bin/env bash

set -eu

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

plugin_name="$(python ../plugin_template/scripts/get_template_config_value.py plugin_name)"
ci_update_docs="$(python ../plugin_template/scripts/get_template_config_value.py ci_update_docs)"
use_black="$(python ../plugin_template/scripts/get_template_config_value.py black)"

if [[ "${ci_update_docs}" == "True" ]]; then
  docs=("--docs")
else
  docs=()
fi

pushd ../plugin_template
pip install -r requirements.txt
./plugin-template --github "${docs[@]}" "${plugin_name}"
popd

if [[ $(git status --porcelain) ]]; then
  git add -A
  git commit -m "Update CI files"
else
  echo "No updates needed"
fi

if [[ "${use_black}" == "True" ]]
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
if [[ "$plugin_name" != "pulpcore" ]]; then
  python ../plugin_template/scripts/update_core_lowerbound.py
  if [[ $(git status --porcelain) ]]; then
    git add -A
    git commit -m "Bump pulpcore lowerbounds to supported branch"
  fi
fi
