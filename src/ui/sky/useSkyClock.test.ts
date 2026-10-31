import { act, renderHook } from '@testing-library/react';
import { CYCLE_MILLISECONDS, SKY_TICK_MILLISECONDS } from './skyClock';
import { useSkyClock } from './useSkyClock';

describe('useSkyClock', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('starts at the chosen theme', () => {
    expect(renderHook(() => useSkyClock('dark')).result.current.phase).toBe(1);
  });

  it('moves on its own as time passes', () => {
    const { result } = renderHook(() => useSkyClock('light'));
    act(() => {
      vi.advanceTimersByTime(CYCLE_MILLISECONDS / 3);
    });

    expect(result.current.phase).toBeCloseTo(1);
  });

  it('counts time from the last trip', () => {
    const { result } = renderHook(() => useSkyClock('light'));
    act(() => {
      vi.advanceTimersByTime(CYCLE_MILLISECONDS / 3);
      result.current.travelTo('simple');
    });

    expect(result.current.phase).toBe(2);

    act(() => {
      vi.advanceTimersByTime(SKY_TICK_MILLISECONDS);
    });

    expect(result.current.phase).toBeLessThan(2.1);
  });

  it('stops the clock when it leaves', () => {
    const { unmount } = renderHook(() => useSkyClock('light'));
    unmount();

    expect(vi.getTimerCount()).toBe(0);
  });
});
