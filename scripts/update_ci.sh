#!/usr/bin/env bash

set -eu

if [ ! -f "template_config.yml" ]; then
  echo "No template_config.yml detected."
  exit 1
fi

plugin_name="$(python ../plugin_template/scripts/get_template_config_value.py plugin_name)"
ci_update_docs="$(python ../plugin_template/scripts/get_template_config_value.py ci_update_docs)"
noissue_marker="$(python ../plugin_template/scripts/get_template_config_value.py noissue_marker)"

if [[ -z "$noissue_marker" ]]; then
  noissue_marker="[noissue]"
fi

if [[ ci_update_docs == "True" ]]; then
  docs="--docs"
else
  docs=""
fi

pushd ../plugin_template
./plugin-template --github $docs $plugin_name
popd

# Check if only gitref file has changed, so no effect on CI workflows.
if [ -z "$(git diff --name-only | grep -v "template_gitref")" ]; then
  echo "No changes detected."
  git ls-files | grep template_gitref | xargs git restore
fi

if [[ $(git status --porcelain) ]]; then
  git add -A
  git commit -m "Update CI files" -m "$noissue_marker"
else
  echo "No updates needed"
fi
