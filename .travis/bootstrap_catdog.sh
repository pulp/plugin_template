#!/usr/bin/env bash

pip install -r test_requirements.txt
./plugin-template --generate-config --plugin-app-label catdog pulp_catdog
mkdir ../pulp_catdog/.travis
touch ../pulp_catdog/.travis/test_bindings.py
echo 'pypi_username: the_pypi_user' >> ../pulp_catdog/template_config.yml
sed -i "s/test_s3: false/test_s3: true/g" ../pulp_catdog/template_config.yml
./plugin-template --all pulp_catdog

cd ../pulp_catdog

# ignore unused imports
sed -i -e '/^ignore/s/$/,F401/' flake8.cfg

# include post_before_script to generate migrations
cp ../plugin_template/.travis/post_before_script.sh .travis/

# generate a git commit
git init
git add .
git commit -m $'Initial commit\n\n[noissue]'
