#!/usr/bin/env sh
set -v

export BEFORE_BEFORE_INSTALL=$TRAVIS_BUILD_DIR/.travis/before_before_install.sh
export AFTER_BEFORE_INSTALL=$TRAVIS_BUILD_DIR/.travis/after_before_install.sh
export BEFORE_BEFORE_SCRIPT=$TRAVIS_BUILD_DIR/.travis/before_before_script.sh
export AFTER_BEFORE_SCRIPT=$TRAVIS_BUILD_DIR/.travis/after_before_script.sh
export AFTER_SCRIPT=$TRAVIS_BUILD_DIR/.travis/after_script.sh
export AFTER_DOCS_TEST=$TRAVIS_BUILD_DIR/.travis/after_docs_test.sh


if [ -f $BEFORE_BEFORE_INSTALL ]; then
    bash $BEFORE_BEFORE_INSTALL
fi

COMMIT_MSG=$(git show HEAD^2 -s)
export COMMIT_MSG
export PULP_PR_NUMBER=$(echo $COMMIT_MSG | grep -oP 'Required\ PR:\ https\:\/\/github\.com\/pulp\/pulpcore\/pull\/(\d+)' | awk -F'/' '{print $7}')
export PULP_PLUGIN_PR_NUMBER=$(echo $COMMIT_MSG | grep -oP 'Required\ PR:\ https\:\/\/github\.com\/pulp\/pulpcore-plugin\/pull\/(\d+)' | awk -F'/' '{print $7}')
export PULP_SMASH_PR_NUMBER=$(echo $COMMIT_MSG | grep -oP 'Required\ PR:\ https\:\/\/github\.com\/PulpQE\/pulp-smash\/pull\/(\d+)' | awk -F'/' '{print $7}')
export PULP_ROLES_PR_NUMBER=$(echo $COMMIT_MSG | grep -oP 'Required\ PR:\ https\:\/\/github\.com\/pulp\/ansible-pulp\/pull\/(\d+)' | awk -F'/' '{print $7}')

# dev_requirements should not be needed for testing; don't install them to make sure
pip install -r test_requirements.txt

{% if not exclude_check_commit_message %}# check the commit message
./.travis/check_commit.sh{% endif %}

# Lint code.
flake8 --config flake8.cfg || exit 1

cd ..
git clone https://github.com/pulp/ansible-pulp.git
if [ -n "$PULP_ROLES_PR_NUMBER" ]; then
  pushd ansible-pulp
  git fetch origin +refs/pull/$PULP_ROLES_PR_NUMBER/merge
  git checkout FETCH_HEAD
  popd
fi

git clone https://github.com/pulp/pulpcore.git

if [ -n "$PULP_PR_NUMBER" ]; then
  pushd pulpcore
  git fetch origin +refs/pull/$PULP_PR_NUMBER/merge
  git checkout FETCH_HEAD
  popd
fi


git clone https://github.com/pulp/pulpcore-plugin.git

if [ -n "$PULP_PLUGIN_PR_NUMBER" ]; then
  pushd pulpcore-plugin
  git fetch origin +refs/pull/$PULP_PLUGIN_PR_NUMBER/merge
  git checkout FETCH_HEAD
  popd
fi


if [ -n "$PULP_SMASH_PR_NUMBER" ]; then
  git clone https://github.com/PulpQE/pulp-smash.git
  pushd pulp-smash
  git fetch origin +refs/pull/$PULP_SMASH_PR_NUMBER/merge
  git checkout FETCH_HEAD
  popd
fi

if [ "$DB" = 'mariadb' ]; then
  # working around https://travis-ci.community/t/mariadb-build-error-with-xenial/3160
  mysql -u root -e "DROP USER IF EXISTS 'travis'@'%';"
  mysql -u root -e "CREATE USER 'travis'@'%';"
  mysql -u root -e "CREATE DATABASE pulp;"
  mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'travis'@'%';";
else
  psql -c 'CREATE DATABASE pulp OWNER travis;'
fi

pip install ansible
cp {{ plugin_snake_name }}/.travis/playbook.yml ansible-pulp/playbook.yml
cp {{ plugin_snake_name }}/.travis/postgres.yml ansible-pulp/postgres.yml
cp {{ plugin_snake_name }}/.travis/mariadb.yml ansible-pulp/mariadb.yml

cd {{ plugin_snake_name }}

if [ -f $AFTER_BEFORE_INSTALL ]; then
    bash $AFTER_BEFORE_INSTALL
fi
