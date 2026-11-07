import type { Rollup } from 'vite';
import { seoPages } from './seoPlugin';

interface Emitted {
  fileName: string;
  source: string;
}

const run = (bundle: Record<string, unknown>): Emitted[] => {
  const emitted: Emitted[] = [];
  const plugin = seoPages();
  const hook = plugin.generateBundle as (this: unknown, options: unknown, bundle: Rollup.OutputBundle) => void;
  hook.call({ emitFile: (file: Emitted) => emitted.push(file) }, {}, bundle as unknown as Rollup.OutputBundle);

  return emitted;
};

describe('SEO pages plugin', () => {
  it('only runs in the build, after the HTML of Vite', () => {
    expect(seoPages()).toMatchObject({ apply: 'build', enforce: 'post' });
  });

  it('turns index.html into the English page and adds the other languages and a sitemap', () => {
    const index = {
      type: 'asset',
      source: '<html lang="en"><head><title>Safira</title></head><body><div id="root"></div></body></html>',
    };
    const emitted = run({ 'index.html': index });

    expect(index.source).toContain('<html lang="en">');
    expect(index.source).toContain('<title>Safira: a programming language in plain words for beginners</title>');
    expect(emitted.map((file) => file.fileName)).toEqual([
      'pt-br/index.html',
      'es/index.html',
      'zh-cn/index.html',
      'ja/index.html',
      'sitemap.xml',
    ]);
    expect(emitted[0]?.source).toContain('<html lang="pt-BR">');
  });

  it.each([
    ['without index.html', {}],
    ['when index.html is not text', { 'index.html': { type: 'asset', source: new Uint8Array() } }],
    ['when index.html is a chunk', { 'index.html': { type: 'chunk' } }],
  ])('stops the build %s', (_case, bundle) => {
    expect(() => run(bundle)).toThrow('index.html is missing from the build');
  });
});
