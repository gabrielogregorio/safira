import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { VariableInspector } from './VariableInspector';

const variables = [
  { name: 'idade', value: '18', type: 'float' },
  { name: 'nome', value: 'Ana', type: 'string' },
];

describe('VariableInspector', () => {
  it('explains what to do when there is nothing yet', () => {
    render(<VariableInspector variables={[]} />);

    expect(screen.getByText('Run your program to see its variables here.')).toBeInTheDocument();
    expect(screen.queryByRole('table')).not.toBeInTheDocument();
  });

  it('shows name, value and type', () => {
    render(<VariableInspector variables={variables} />);

    expect(screen.getByRole('row', { name: 'idade 18 float' })).toBeInTheDocument();
  });

  it('filters by name ignoring case', async () => {
    render(<VariableInspector variables={variables} />);
    await userEvent.type(screen.getByLabelText('Search variables'), 'NO');

    expect(screen.queryByRole('cell', { name: 'idade' })).not.toBeInTheDocument();
    expect(screen.getByRole('cell', { name: 'nome' })).toBeInTheDocument();
  });
});
