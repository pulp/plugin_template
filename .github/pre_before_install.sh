#!/usr/bin/env bash

echo ::group::test_requirements
pip install -r test_requirements.txt
echo ::endgroup::
./plugin-template --generate-config --plugin-app-label catdog pulp_catdog
mkdir ../pulp_catdog/.github
mkdir ../pulp_catdog/.travis # due to test_bindings
touch ../pulp_catdog/.travis/test_bindings.py # due to test_bindings
echo 'pypi_username: the_pypi_user' >> ../pulp_catdog/template_config.yml
./plugin-template --all pulp_catdog
mv ../pulp_catdog/*.txt .
mv ../pulp_catdog/.github/before_install.sh ../pulp_catdog/.github/old_before_install.sh
find ../pulp_catdog/.github -type f -exec mv {} ./.github/ \;
