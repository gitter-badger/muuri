#!/bin/bash 
export VENV="$(dirname $(readlink -f "$0"))"
cd $VENV

find . -type d -iname "__pycache__" -exec bash -c "echo rm -rf '{}'" \;
find . -type f -iname "*.pyc" -delete

cd -
