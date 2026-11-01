import { act, renderHook } from '@testing-library/react';
import { navigateTo, useRoute } from './useRoute';

describe('useRoute', () => {
  beforeEach(() => {
    window.history.replaceState(null, '', '#/');
  });

  it('reads the current address', () => {
    window.history.replaceState(null, '', '#/new');

    expect(renderHook(() => useRoute()).result.current.route).toMatchObject({ name: 'new' });
  });

  it('changes the address and the route together', () => {
    const { result } = renderHook(() => useRoute());
    act(() => {
      result.current.navigate({ name: 'new', exampleId: null });
    });

    expect(window.location.hash).toBe('#/new');
    expect(result.current.route).toEqual({ name: 'new', exampleId: null });
  });

  it('does not add a history entry for the current address', () => {
    const before = window.history.length;
    navigateTo({ name: 'home' });

    expect(window.history).toHaveLength(before);
  });

  it('follows the browser buttons', () => {
    const { result } = renderHook(() => useRoute());
    act(() => {
      window.history.replaceState(null, '', '#/new');
      window.dispatchEvent(new HashChangeEvent('hashchange'));
    });

    expect(result.current.route.name).toBe('new');
  });
});
