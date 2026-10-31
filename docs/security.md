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
- A recursion limit stops functions that never end, and the Stop button terminates the worker.

## Accepted risks

Accepted by alert id, so a new alert on the same package still counts. Review date: 2027-01-31.

| Alert | Package | Severity | Why it is accepted |
|---|---|---|---|

## Dependency rules

- New versions wait 3 days before they can be installed.
- Every install is checked against the hashes in the lockfile.
- Install scripts are blocked except for the listed packages.
- Actions are pinned to a commit hash, and CI fails when one is not.
