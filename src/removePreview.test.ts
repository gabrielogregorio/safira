import { execFileSync, spawnSync } from 'node:child_process';
import { chmodSync, existsSync, mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

const GIT = '/usr/bin/git';
const SCRIPT = resolve('.github/scripts/remove-preview.sh');
const IDENTITY = ['-c', 'user.name=t', '-c', 'user.email=t@t'];
const REJECT_ONCE = `#!/usr/bin/env bash
if [ ! -f "$GIT_DIR/rejected" ]; then
  touch "$GIT_DIR/rejected"
  exit 1
fi
`;

interface Site {
  work: string;
  origin: string;
  commits: () => number;
  published: (path: string) => boolean;
}

const siteWith = (paths: string[]): Site => {
  const folder = mkdtempSync(join(tmpdir(), 'safira-preview-'));
  const origin = join(folder, 'origin.git');
  const work = join(folder, 'work');
  const git = (...args: string[]) => execFileSync(GIT, args, { cwd: work, stdio: 'ignore' });
  execFileSync(GIT, ['init', '--bare', '--quiet', '--initial-branch=gh-pages', origin]);
  mkdirSync(work);
  git('init', '--quiet', '--initial-branch=gh-pages');
  git('remote', 'add', 'origin', origin);

  for (const path of paths) {
    mkdirSync(join(work, path, '..'), { recursive: true });
    writeFileSync(join(work, path), 'x');
  }

  git('add', '.');
  git(...IDENTITY, 'commit', '--quiet', '-m', 'site');
  git('push', '--quiet', 'origin', 'gh-pages');

  const read = (...args: string[]) => execFileSync(GIT, args, { cwd: origin, encoding: 'utf8' });

  return {
    work,
    origin,
    commits: () => Number(read('rev-list', '--count', 'gh-pages')),
    published: (path) => read('ls-tree', '-r', '--name-only', 'gh-pages').split('\n').includes(path),
  };
};

const run = (branch: string, site: Site) =>
  spawnSync(SCRIPT, [], {
    cwd: site.work,
    encoding: 'utf8',
    env: { ...process.env, HEAD_REF: branch, RETRY_SECONDS: '0' },
  });

describe('remove-preview.sh', () => {
  it('removes the preview of the branch and nothing else', () => {
    const site = siteWith([
      'index.html',
      'preview/one/index.html',
      'preview/one/assets/a.js',
      'preview/two/index.html',
    ]);

    expect(run('one', site).status).toBe(0);
    expect(site.published('preview/one/index.html')).toBe(false);
    expect(site.published('preview/one/assets/a.js')).toBe(false);
    expect(site.published('preview/two/index.html')).toBe(true);
    expect(site.published('index.html')).toBe(true);
  });

  it('names the preview after the last part of the branch, as the deploy does', () => {
    const site = siteWith(['preview/one/index.html', 'preview/feature/index.html']);

    expect(run('feature/one', site).status).toBe(0);
    expect(site.published('preview/one/index.html')).toBe(false);
    expect(site.published('preview/feature/index.html')).toBe(true);
  });

  it('changes nothing when the branch has no preview', () => {
    const site = siteWith(['index.html']);

    expect(run('one', site).status).toBe(0);
    expect(site.commits()).toBe(1);
  });

  it('tries again when gh-pages moved during the removal', () => {
    const site = siteWith(['preview/one/index.html', 'index.html']);
    const hook = join(site.origin, 'hooks', 'pre-receive');
    writeFileSync(hook, REJECT_ONCE);
    chmodSync(hook, 0o755);

    const { status, stdout } = run('one', site);

    expect(status).toBe(0);
    expect(stdout).toContain('trying again');
    expect(site.published('preview/one/index.html')).toBe(false);
  });

  it.each(['..', '.', 'a;b', 'a b', '$(id)', 'x/..'])('refuses a branch called %s', (branch) => {
    const site = siteWith(['index.html', 'preview/one/index.html']);

    expect(run(branch, site).status).toBe(1);
    expect(site.commits()).toBe(1);
    expect(existsSync(join(site.work, 'index.html'))).toBe(true);
  });
});
