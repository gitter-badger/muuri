#!/bin/sh
export VENV="$(dirname $(readlink -f "$0"))"
python3 -m venv $VENV

$VENV/bin/python3 ws/wsserver.py
