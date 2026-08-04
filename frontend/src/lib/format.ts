export function formatMassKg(value: number): string {
  return `${value.toFixed(3)} kg`;
}

export function formatVolumeM3(value: number): string {
  return `${value.toExponential(3)} m3`;
}

export function formatLengthM(value: number): string {
  return `${value.toFixed(3)} m`;
}

export function formatTensorValue(value: number): string {
  return value.toExponential(3);
}
