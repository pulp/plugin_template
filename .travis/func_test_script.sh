#!/usr/bin/env bash
# coding=utf-8

set -mveuo pipefail

cd ../pulp_catdog
pytest -v -r sx --color=yes --pyargs pulp_catdog.tests.functional || show_logs_and_return_non_zero
