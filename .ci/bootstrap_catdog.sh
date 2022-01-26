#!/usr/bin/env bash

set -euv

GITHUB_EVENT_NAME="${GITHUB_EVENT_NAME:-not_pull_request}"
if [ "$GITHUB_EVENT_NAME" = "pull_request" ]
then
    COMMIT_MSG=$(git log --format=%B -n 1 HEAD^2)
else
    COMMIT_MSG="Initial commit\n\n[noissue]"
fi
echo $COMMIT_MSG

pip install -r test_requirements.txt
./plugin-template --generate-config --plugin-app-label catdog pulp_catdog
mkdir -p ../pulp_catdog/.ci/assets/bindings
touch ../pulp_catdog/.ci/assets/bindings/test_bindings.py
touch ../pulp_catdog/.ci/assets/bindings/test_bindings.rb
echo 'pypi_username: the_pypi_user' >> ../pulp_catdog/template_config.yml
sed -i "s/test_s3: false/test_s3: true/g" ../pulp_catdog/template_config.yml
sed -i "s/test_azure: false/test_azure: true/g" ../pulp_catdog/template_config.yml
sed -i "s/test_bindings: true/test_bindings: false/g" ../pulp_catdog/template_config.yml
sed -i "s/disabled_redis_runners: \[\]/disabled_redis_runners: [s3]/g" ../pulp_catdog/template_config.yml
./plugin-template --all pulp_catdog

cd ../pulp_catdog

# ignore unused imports
flake8 .ci || exit 1 # check ci files before ignoring imports
sed -i -e '/^ignore/s/$/,F401/' .flake8

# include post_before_script to generate migrations
cp ../plugin_template/.ci/post_before_script.sh .github/workflows/scripts

# generate a git commit
git init
git config user.name "Cat Dog"
git config user.email "pulp@cat.dog"
git add .
git commit -m "$COMMIT_MSG"
