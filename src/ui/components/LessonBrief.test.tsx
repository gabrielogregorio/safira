import { render, screen } from '@testing-library/react';
import { describeFailure, LessonBrief } from './LessonBrief';
import { createTranslator } from '@/i18n/i18n';

const t = createTranslator('en-us');
const step = {
  title: 'Passo',
  text: 'Use `mostre`.',
  code: '',
  solution: 'mostre 1',
  check: { hint: 'Use o mostre', cases: [] },
};
const actions = { onNext: vi.fn(), onBack: vi.fn(), onStartOver: vi.fn(), onShowSolution: vi.fn() };
const base = { step, isDone: false, isLastStep: false, isOnStepFile: true, ...actions };

describe('LessonBrief', () => {
  it('renders the explanation as markdown', () => {
    render(<LessonBrief {...base} verdict={{ status: 'idle' }} />);

    expect(screen.getByText('mostre').tagName).toBe('CODE');
  });

  it('shows that it is checking', () => {
    render(<LessonBrief {...base} verdict={{ status: 'checking' }} />);

    expect(screen.getByRole('status')).toHaveTextContent('Checking your answer...');
  });

  it('only offers the solution after a failure', () => {
    const { rerender } = render(<LessonBrief {...base} verdict={{ status: 'idle' }} />);

    expect(screen.queryByRole('button', { name: 'Show the solution' })).not.toBeInTheDocument();

    rerender(
      <LessonBrief
        {...base}
        verdict={{ status: 'failed', result: { passed: false, reason: 'command', text: '', inputs: [] } }}
      />,
    );

    expect(screen.getByRole('button', { name: 'Show the solution' })).toBeInTheDocument();
    expect(screen.getByText('Tip: Use o mostre')).toBeInTheDocument();
  });

  it('ends the course on the last step', () => {
    render(<LessonBrief {...base} isDone isLastStep verdict={{ status: 'idle' }} />);

    expect(screen.getByRole('status')).toHaveTextContent('You finished every lesson! 🎉');
    expect(screen.queryByRole('button', { name: 'Next' })).not.toBeInTheDocument();
  });
});

describe('describeFailure', () => {
  const failed = { passed: false, inputs: [] } as const;

  it.each([
    [{ ...failed, reason: 'missing', text: '8' }, 'Almost! "8" did not appear in the output.'],
    [{ ...failed, reason: 'missing', text: '8', inputs: ['4'] }, 'Almost! When the answer is 4, "8" should appear.'],
    [{ ...failed, reason: 'unexpected', text: 'par' }, 'Almost! "par" should not appear here.'],
    [{ ...failed, reason: 'error', text: 'Falhou', line: 2 }, 'Line 2: Falhou'],
    [{ ...failed, reason: 'limit', text: '' }, 'Your program never ends. Check your repetition.'],
    [{ ...failed, reason: 'command', text: '' }, ''],
  ] as const)('explains %j', (result, message) => {
    expect(describeFailure(t, { ...result, inputs: [...result.inputs] })).toBe(message);
  });
});
