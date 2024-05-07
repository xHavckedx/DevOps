#!/bin/bash
git config --global user.email "leo.gomez@cttexpress.com"
git config --global user.name "Leo G�mez"
git clone https://$gitops_username:$gitops_access_token@$azure_repo gitops
cd gitops
tag_version=$(git describe --tags $(git rev-list --tags --max-count=1)) # me devuelve el tag de la última versión suele ser: v1.0.0
tag_new_version=$(echo $tag_version | awk -F'.' '{$2++; print}' OFS='.') # incrementa la versión de tipo minor
git tag $tag_new_version
git-chglog -o CHANGELOG.md
git add CHANGELOG.md
git commit -m "New release $tag_new_version"
git push -f
git push --tags
