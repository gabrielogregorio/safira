import golden from './legacyGolden.json';
import type { RecordedEvent } from './testHarness';
import { runScript } from './testHarness';

interface GoldenCase {
  name: string;
  source: string;
  inputs: string[];
  events: RecordedEvent[];
  error: boolean;
}

const WHOLE_FLOAT_SUFFIX = /(?<![\w.])(\d+)\.0(?!\d)/g;

const normalizeLegacyText = (text: string): string => text.replace(WHOLE_FLOAT_SUFFIX, '$1');

const normalizeLegacyEvent = (event: RecordedEvent): RecordedEvent =>
  event.text === undefined ? event : { ...event, text: normalizeLegacyText(event.text) };

const cases: GoldenCase[] = golden as GoldenCase[];

describe('parity with the recordings of the legacy interpreter', () => {
  it.each(cases.map((goldenCase) => [goldenCase.name, goldenCase] as const))('%s', async (_name, goldenCase) => {
    const result = await runScript(goldenCase.source, goldenCase.inputs);

    expect(result.events).toEqual(goldenCase.events.map(normalizeLegacyEvent));
    expect(result.error !== null).toBe(goldenCase.error);
  });
});
