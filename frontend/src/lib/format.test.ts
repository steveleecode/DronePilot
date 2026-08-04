import { describe, expect, it } from 'vitest';

import { formatLengthM, formatMassKg, formatTensorValue, formatVolumeM3 } from './format';

describe('engineering value formatting', () => {
  it('formats mass, volume, length, and inertia tensor values', () => {
    expect(formatMassKg(0.886492)).toBe('0.886 kg');
    expect(formatVolumeM3(0.000554057)).toBe('5.541e-4 m3');
    expect(formatLengthM(0.488996)).toBe('0.489 m');
    expect(formatTensorValue(0.0058721)).toBe('5.872e-3');
  });
});
