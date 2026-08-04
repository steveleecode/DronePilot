import type { DroneAnalysis, DroneModelMetadata } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`);
  }
  return (await response.json()) as T;
}

export function resolveApiUrl(path: string): string {
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  return `${API_BASE_URL}${path}`;
}

export function fetchDroneModel(): Promise<DroneModelMetadata> {
  return getJson<DroneModelMetadata>('/api/v1/models/v1-drone');
}

export function fetchDroneAnalysis(): Promise<DroneAnalysis> {
  return getJson<DroneAnalysis>('/api/v1/models/v1-drone/analysis');
}
