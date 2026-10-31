# Contributing

Setup and scripts are in the [README](README.md).

1. Branch from `dev` and open the pull request to `dev`.
2. Add tests with the behavior. A bug fix brings a regression test.
3. Run `pnpm run check:all`.
4. To release, bump `version` in `package.json` and open a pull request from `dev` to `master`.
