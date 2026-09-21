#!/bin/bash

set -e

echo "Building Evolution Simulator..."
rm -rf build dist
python3.11 -m PyInstaller main.spec

echo "Uploading to itch.io..."
/Applications/butler push \
"dist/Evolution Simulator.app" \
twinkledelux/evosim:mac

echo "Done!"

