# Contributing

Setup and scripts are in the [README](README.md).

1. Branch from `dev` and open the pull request to `dev`.
2. Add tests with the behavior. A bug fix brings a regression test.
3. Run `pnpm run check:all`.
4. To release, create `release/X.Y.Z` from `dev`, set the same version in `package.json` and open a pull request to
   `main`. Any other pull request merges without a version and without a release.

## Rules that break a pull request

- A new command goes in `commands.json`, in `scenarios.ts` and in all five dictionaries of `dialects.ts`.
- A new example or lesson goes in all five folders of `src/content`, with the same file name.
- Interface text goes through `t()`, with an entry for all five languages.
- Never regenerate `legacyGolden.json` and never rewrite `legacyExamples`: they prove old scripts still work.
- Never lower a coverage floor or an accessibility floor to make a check pass.
- Browser data goes through `storageKey`, and a reset only removes its own prefix.
- Commits are one line in English, with no conventional prefix.
