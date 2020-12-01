#!/usr/bin/env bash

set -euv

pip install -r test_requirements.txt
./plugin-template --generate-config --plugin-app-label catdog pulp_catdog
mkdir -p ../pulp_catdog/.ci/assets/bindings
touch ../pulp_catdog/.ci/assets/bindings/test_bindings.py
touch ../pulp_catdog/.ci/assets/bindings/test_bindings.rb
echo 'pypi_username: the_pypi_user' >> ../pulp_catdog/template_config.yml
sed -i "s/test_s3: false/test_s3: true/g" ../pulp_catdog/template_config.yml
./plugin-template --all pulp_catdog

cd ../pulp_catdog

# ignore unused imports
flake8 --config flake8.cfg .ci || exit 1 # check travis files before ignoring imports
sed -i -e '/^ignore/s/$/,F401/' flake8.cfg

# include post_before_script to generate migrations
cp ../plugin_template/.ci/post_before_script.sh .github/workflows/scripts

# generate a git commit
git init
git config user.name "Cat Dog"
git config user.email "pulp@cat.dog"
git add .
git commit -m $'Initial commit\n\n[noissue]'
