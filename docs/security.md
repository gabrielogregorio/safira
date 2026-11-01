# Security

## Supported versions

Only the latest release gets fixes.

## Reporting a vulnerability

Do not open a public issue. Use the private form in the Security tab of this repository, under "Report a vulnerability".
Include the version, the steps and the impact.

## What protects what

- Programs run in a Web Worker, without access to the page.
- The interpreter walks a syntax tree. There is no `eval` or `Function`, and no way to reach JavaScript from Safira.
- Files are virtual, kept per project. The language has no access to disk, network or browser storage.
- Output is rendered as text by React.
- An imported `.zip` is limited to 500 files and 4 MB, paths that leave the project are refused and binary files are skipped.
- Lesson markdown ignores raw HTML.
- A recursion limit stops functions that never end, and the Stop button terminates the worker.

## Stored data

Nothing is collected or sent anywhere: projects and settings stay in this browser. The site and its previews share one origin, so each preview uses its own storage keys. That prevents accidents, not reading: code in a preview could read the data of the site, which is why previews are only published from branches of this repository, never from forks.

## Pipeline

- No workflow uses `pull_request_target`, and pull requests from forks get a read-only token and no secrets.
- Actions are pinned to a commit hash, and event data reaches scripts through `env`.
- Jobs that build keep the token away from the build with `persist-credentials: false`, so a compromised package cannot
  write to the repository. `check-quality.yml` fails if a workflow breaks this rule.
- A version only reaches `$GITHUB_ENV` after `.github/scripts/release-version.sh` validates it.

## Accepted risks

Accepted by alert id, so a new alert on the same package still counts. Review date: 2027-01-31.

| Alert | Package | Severity | Why it is accepted |
|---|---|---|---|

## Dependency rules

- New versions wait 3 days before they can be installed.
- Every install is checked against the hashes in the lockfile.
- Install scripts are blocked except for the listed packages.
- Actions are pinned to a commit hash, and CI fails when one is not.
