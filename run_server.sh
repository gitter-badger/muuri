#!/bin/sh -e
export VENV="$(dirname $(readlink -f "$0"))"
python3 -m venv $VENV

$VENV/bin/pserve "development.ini" --reload --verbose
