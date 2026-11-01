## What changes

<!-- one or two lines: what the user notices -->

## Changelog

[...autoGenerate]

## Checklist

- [ ] Release? The branch is `release/X.Y.Z` and `package.json` says the same (no other PR needs a version)
- [ ] `pnpm run check:all` passes, and the coverage floor was not lowered
- [ ] New UI text goes through `t('…')`, with an entry for all five languages in `src/i18n`
- [ ] A new command is in `commands.json`, `scenarios.ts` and all five dictionaries of `dialects.ts`
- [ ] A new example or lesson exists in all five folders of `src/content`
