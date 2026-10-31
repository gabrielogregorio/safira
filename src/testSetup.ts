import '@testing-library/jest-dom/vitest';

class ResizeObserverStub {
  public observe(): void {}

  public unobserve(): void {}

  public disconnect(): void {}
}

globalThis.ResizeObserver = ResizeObserverStub;
Element.prototype.scrollIntoView = (): void => undefined;
Element.prototype.scrollTo = (): void => undefined;
Element.prototype.hasPointerCapture = (): boolean => false;
Element.prototype.releasePointerCapture = (): void => undefined;
Range.prototype.getClientRects = (): DOMRectList => [] as unknown as DOMRectList;
Range.prototype.getBoundingClientRect = (): DOMRect => new DOMRect();

// jsdom has no canvas, so the logo falls back to its flat version in tests.
HTMLCanvasElement.prototype.getContext = (() => null) as typeof HTMLCanvasElement.prototype.getContext;
