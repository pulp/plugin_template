#!/bin/sh

$CMD_PREFIX pulpcore-manager makemigrations
$CMD_PREFIX pulpcore-manager migrate
