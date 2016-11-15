#!/bin/bash -e
export VENV="$(dirname $(readlink -f "$0"))"

python3 -m venv $VENV

LOCALEDIR="$(dirname $(readlink -f "$0"))/muuri/locale"
LOCALEPOT="$LOCALEDIR/default.pot"

echo "Generating '$LOCALEPOT'"
strace -e trace=open $VENV/bin/pot-create --package-name "muuri" --package-version "1.0" --output "$LOCALEPOT" "muuri"
echo ""

cd "$LOCALEDIR"

echo "Updating .po files.."
find . -type f -iname "*.po" -exec bash -c "echo 'file: {}'; msgmerge --update '{}' '$LOCALEPOT'" \;
echo ""

echo "Generating .mo files.."
find . -type f -iname "*.po" -print0 | while read -d '' -r file; do 
  MOFILE="${file%.*}.mo"
  echo "${file} -> $MOFILE"
  msgfmt "${file}" -o "$MOFILE" 
done
echo ""

echo "Listing files:"
find . -type f 
echo ""

cd -

echo "Done."
