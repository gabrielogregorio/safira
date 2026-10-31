import { execFileSync, spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

const GIT = '/usr/bin/git';
const SCRIPT = resolve('.github/scripts/release-version.sh');
const NEWLINE_VERSION = '1.0.0\nLD_PRELOAD=/tmp/evil.so';

const repositoryWith = (version: string, tags: string[] = []): string => {
  const folder = mkdtempSync(join(tmpdir(), 'safira-release-'));
  const origin = join(folder, 'origin.git');
  const work = join(folder, 'work');
  const git = (...args: string[]) => execFileSync(GIT, args, { cwd: work, stdio: 'ignore' });
  execFileSync(GIT, ['init', '--bare', '--quiet', origin]);
  mkdirSync(work);
  git('init', '--quiet');
  git('remote', 'add', 'origin', origin);
  writeFileSync(join(work, 'package.json'), JSON.stringify({ version }));

  for (const tag of tags) {
    git('add', '.');
    git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '--quiet', '-m', 'x');
    git('tag', tag);
    git('push', '--quiet', 'origin', tag);
  }

  return work;
};

const run = (branch: string, folder: string) => spawnSync(SCRIPT, [branch], { cwd: folder, encoding: 'utf8' });

describe('release-version.sh', () => {
  it('prints the version of a valid release branch', () => {
    const { status, stdout } = run('release/1.2.3', repositoryWith('1.2.3'));

    expect(status).toBe(0);
    expect(stdout.trim()).toBe('1.2.3');
  });

  it('accepts a prerelease', () => {
    expect(run('release/1.2.3-rc.1', repositoryWith('1.2.3-rc.1')).status).toBe(0);
  });

  it.each(['dev', 'release/1.2', 'release/v1.2.3', 'release/1.2.3;id', 'release/1.2.3 x'])('refuses %s', (branch) => {
    expect(run(branch, repositoryWith('1.2.3')).status).toBe(1);
  });

  it('refuses a version that differs from the branch', () => {
    expect(run('release/1.2.3', repositoryWith('1.2.4')).stderr).toContain("package.json says '1.2.4'");
  });

  it('refuses a version with a line break, so that nothing reaches $GITHUB_ENV', () => {
    const { status, stdout } = run('release/1.0.0', repositoryWith(NEWLINE_VERSION));

    expect(status).toBe(1);
    expect(stdout).toBe('');
  });

  it('refuses a version that is already released', () => {
    expect(run('release/1.2.3', repositoryWith('1.2.3', ['v1.2.3'])).stderr).toContain('already released');
  });
});
