import {
  collectTextNodes,
  randomCharacter,
  randomCharacterLike,
  scrambleDocument,
  scrambleFrame,
} from './textScramble';

const pickX = (): string => 'x';

describe('scrambleFrame', () => {
  it('hides every letter at the start', () => {
    expect(scrambleFrame('abcd', 0, pickX)).toBe('xxxx');
  });

  it('reveals the text from the left as it advances', () => {
    expect(scrambleFrame('abcd', 0.5, pickX)).toBe('abxx');
  });

  it('shows the final text at the end', () => {
    expect(scrambleFrame('abcd', 1, pickX)).toBe('abcd');
  });

  it('keeps spaces so that words hold their shape', () => {
    expect(scrambleFrame('a b c', 0, pickX)).toBe('x x x');
  });

  it('scrambles ideographs among ideographs and Latin letters among Latin letters', () => {
    expect(randomCharacterLike('语')).toMatch(/^[\u3040-\u30ff\u3400-\u9fff]$/);
    expect(randomCharacterLike('a')).toMatch(/^[\x21-\x7e]$/);
  });

  it('picks a single visible character', () => {
    expect(randomCharacter()).toMatch(/^\S$/);
  });
});

describe('collectTextNodes', () => {
  it('takes interface text, even behind a modal, and leaves code and terminal alone', () => {
    document.body.innerHTML = `
      <p>interface</p>
      <div class="cm-editor">codigo</div>
      <div class="terminal-log">saida</div>
      <div aria-hidden="true">atras do modal</div>
    `;

    expect(collectTextNodes(document.body).map((node) => node.nodeValue)).toEqual(['interface', 'atras do modal']);
  });
});

describe('collectTextNodes with fixed text', () => {
  it('leaves names that are not translated alone', () => {
    document.body.innerHTML = '<p>interface</p><span data-fixed-text>Meu projeto</span>';

    expect(collectTextNodes(document.body).map((node) => node.nodeValue)).toEqual(['interface']);
  });

  it('still takes a translated control inside fixed content', () => {
    document.body.innerHTML = '<div data-fixed-text><p>aula</p><button data-translated>Open</button></div>';

    expect(collectTextNodes(document.body).map((node) => node.nodeValue)).toEqual(['Open']);
  });
});

describe('scrambleDocument', () => {
  it('still plays when the first frame arrives after the time of the whole animation', () => {
    const frames: FrameRequestCallback[] = [];
    const request = vi.spyOn(window, 'requestAnimationFrame').mockImplementation((callback) => frames.push(callback));
    const root = document.createElement('div');
    root.textContent = 'Criar projeto';
    scrambleDocument(root);

    frames.at(-1)?.(performance.now() + 5000);
    expect(root.textContent).not.toBe('Criar projeto');

    frames.at(-1)?.(performance.now() + 6000);
    expect(root.textContent).toBe('Criar projeto');
    request.mockRestore();
  });

  it('keeps a text written after the animation ended when it is cancelled', () => {
    const root = document.createElement('div');
    root.textContent = 'Criar projeto';
    const cancel = scrambleDocument(root);
    (root.firstChild as Text).nodeValue = 'Crear proyecto';
    cancel();

    expect(root.textContent).toBe('Crear proyecto');
  });

  it('restores the exact text when cancelled', () => {
    document.body.innerHTML = '<p>Olá mundo</p>';
    vi.stubGlobal('requestAnimationFrame', () => 1);
    vi.stubGlobal('cancelAnimationFrame', vi.fn());
    const cancel = scrambleDocument(document.body);
    cancel();

    expect(document.body.textContent).toBe('Olá mundo');
    vi.unstubAllGlobals();
  });

  it('runs until the text is final', () => {
    document.body.innerHTML = '<p>abc</p>';
    const frames: FrameRequestCallback[] = [];
    vi.stubGlobal('requestAnimationFrame', (callback: FrameRequestCallback) => frames.push(callback));
    scrambleDocument(document.body);
    (frames.shift() as FrameRequestCallback)(0);
    (frames.shift() as FrameRequestCallback)(100_000);

    expect(document.body.textContent).toBe('abc');
    expect(frames).toHaveLength(0);
    vi.unstubAllGlobals();
  });
});
