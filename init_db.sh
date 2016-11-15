#!/bin/bash
export VENV="$(dirname $(readlink -f "$0"))"
INIFILE="development.ini"
INISECTION="app:main"

cd $VENV

echo "Upgrading packages:"
./upgrade_packages.sh

echo ""
echo "--------------------"
echo ""

echo "Clearing cache files.."
./rm_python_cache.sh

echo ""
echo "--------------------"
echo ""

python3 -m venv $VENV

echo "Removing old DB:"
$VENV/bin/alembic --raiseerr --config "$INIFILE" --name "$INISECTION" downgrade head

echo ""
echo "--------------------"
echo ""

echo "Removing database init:"
find "./alembic/versions/" -type f -iname "1_init.py" -delete

echo ""
echo "--------------------"
echo ""

echo "Running init database:"
$VENV/bin/alembic --raiseerr --config "$INIFILE" --name "$INISECTION" revision --autogenerate --message "init" --rev-id 1

echo ""
echo "--------------------"
echo ""

cat "./alembic/versions/1_init.py"

echo ""
echo "--------------------"
echo ""

echo "Initiliazing DB:"
$VENV/bin/alembic --raiseerr --config "$INIFILE" --name "$INISECTION" upgrade head

echo ""
echo "--------------------"
echo ""

# Back to starting directory
cd -

echo "Done."
echo ""
