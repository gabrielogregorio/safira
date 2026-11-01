#!/usr/bin/env bash
# Removes preview/<branch> from a checkout of gh-pages, and tries again when another workflow published at the same time.
set -euo pipefail

name="${HEAD_REF##*/}"

if [[ ! "$name" =~ ^[A-Za-z0-9._-]+$ || "$name" == "." || "$name" == ".." ]]; then
  echo "::error::refusing to remove a preview called '$name'"
  exit 1
fi

target="preview/$name"

for attempt in 1 2 3 4 5; do
  git fetch --quiet origin gh-pages
  git reset --quiet --hard FETCH_HEAD

  if [[ ! -d "$target" ]]; then
    echo "No preview at $target"
    exit 0
  fi

  git rm -r --quiet "$target"
  git -c user.name=github-actions-bot -c user.email=support+actions@github.com \
    commit --quiet -m "Remove the preview of $name"

  if git push --quiet origin HEAD:gh-pages; then
    exit 0
  fi

  echo "::warning::gh-pages moved during the removal, trying again ($attempt of 5)"
  sleep $((attempt * ${RETRY_SECONDS:-10}))
done

exit 1
