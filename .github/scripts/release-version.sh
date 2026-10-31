#!/usr/bin/env bash
# Prints the version a release branch publishes, or refuses the branch.
set -euo pipefail

BRANCH="${1:?usage: release-version.sh release/X.Y.Z}"
VERSION="${BRANCH#release/}"
SEMVER='^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.]+)?$'

refuse() {
  echo "::error::$1" >&2
  exit 1
}

if [[ "$BRANCH" != release/* || ! "$VERSION" =~ $SEMVER ]]; then
  refuse "'$BRANCH' is not a release branch: name it release/X.Y.Z or release/X.Y.Z-rc.1"
fi

FILE_VERSION=$(node -p "require('./package.json').version")
if [[ "$FILE_VERSION" != "$VERSION" ]]; then
  refuse "package.json says '$FILE_VERSION' but the branch says '$VERSION'"
fi

if git ls-remote --exit-code --tags origin "refs/tags/v$VERSION" > /dev/null; then
  refuse "v$VERSION is already released: raise the version in the branch name and in package.json"
fi

echo "$VERSION"
