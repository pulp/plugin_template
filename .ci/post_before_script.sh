#!/bin/sh

set -eu

cmd_prefix pulpcore-manager makemigrations
cmd_user_prefix pulpcore-manager migrate
