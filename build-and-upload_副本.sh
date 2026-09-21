#!/bin/bash
set -e

USER_VERSION=""

for arg in "$@"; do
    case $arg in
        --userversion=*)
            USER_VERSION="${arg#*=}"
            ;;
    esac
done

if [ -z "$USER_VERSION" ]; then
    read -p "Enter version number: " USER_VERSION
fi

echo "Building Evolution Simulator v$USER_VERSION..."

rm -rf build dist
python3.11 -m PyInstaller --clean main.spec

BUTLER="/Applications/butler"

echo "Logging into Butler..."
"$BUTLER" login

echo "Uploading to itch.io..."
"$BUTLER" push \
"dist/Evolution Simulator.app" \
twinkledelux/evosim:mac \
--userversion="$USER_VERSION"

echo "Successfully uploaded v$USER_VERSION!"