#!/usr/bin/env sh
set -v

if [ -f $BEFORE_BEFORE_SCRIPT ]; then
    bash $BEFORE_BEFORE_SCRIPT
fi


mkdir -p ~/.config/pulp_smash
cp ../pulpcore/.travis/pulp-smash-config.json ~/.config/pulp_smash/settings.json


if [ -f $AFTER_BEFORE_SCRIPT ]; then
    bash $AFTER_BEFORE_SCRIPT
fi
