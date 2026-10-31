import { collectTextNodes, randomCharacter, scrambleDocument, scrambleFrame } from './textScramble';

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

describe('scrambleDocument', () => {
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
    (frames.shift() as FrameRequestCallback)(performance.now() + 100_000);

    expect(document.body.textContent).toBe('abc');
    expect(frames).toHaveLength(0);
    vi.unstubAllGlobals();
  });
});
