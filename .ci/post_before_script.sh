#!/bin/sh

set -euv

cmd_prefix pulpcore-manager makemigrations
cmd_user_prefix pulpcore-manager migrate
