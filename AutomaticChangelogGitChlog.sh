#!/bin/bash

tag_version=git describe --tags $(git rev-list --tags --max-count=1) # me devuelve el tag de la última versión suele ser: v1.0.0

tag_new_version=echo $tag_vesion | awk -F'.' '{$2++; print}' OFS='.' # incrementa la versión de tipo minor

git-chglog -o CHANGELOG.md

git add CHANGELOG.md
git commit -m "New release $tag_new_version"
git push
