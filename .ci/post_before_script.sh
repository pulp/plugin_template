#!/bin/sh

cmd_prefix pulpcore-manager makemigrations
cmd_prefix pulpcore-manager migrate
