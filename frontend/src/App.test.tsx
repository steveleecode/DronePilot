import { render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { App } from './App';

vi.mock('./features/viewer/DroneScene', () => ({
  DroneScene: () => <div aria-label="mock drone scene" />,
}));

const sampleAnalysis = {
  model_id: 'v1-drone',
  part_count: 300,
  total_volume_m3: 0.0005540579326155427,
  total_mass_kg: 0.8864926921848683,
  center_of_gravity_m: { x: -0.229, y: 0.005, z: 0.033 },
  inertia_tensor_kg_m2: [
    [0.005, 0, 0],
    [0, 0.011, 0],
    [0, 0, 0.017],
  ],
  principal_moments_kg_m2: [0.005, 0.011, 0.017],
  bounding_box_m: { x: 0.489, y: 0.5, z: 0.101 },
  materials: [],
  parts: [],
  warnings: ['Imported as one compound.'],
  metadata: {
    source_step_path: 'cad/v1-drone.step',
    source_length_unit: 'millimeter',
    coordinate_convention: '+x right, +y forward, +z up',
    unit_convention: 'SI',
    processing_version: '0.1.0',
    default_material_id: 'carbon-fiber',
  },
};

beforeEach(() => {
  vi.stubGlobal(
    'fetch',
    vi.fn((url: string) => {
      if (url.endsWith('/api/v1/models/v1-drone')) {
        return Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              model_id: 'v1-drone',
              source_step_path: 'cad/v1-drone.step',
              analysis_url: '/api/v1/models/v1-drone/analysis',
              geometry_url: '/api/v1/models/v1-drone/geometry.glb',
            }),
        });
      }

      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(sampleAnalysis),
      });
    }),
  );
});

describe('App', () => {
  it('loads and displays engineering properties from the API', async () => {
    render(<App />);

    await waitFor(() => expect(screen.getByText('CAD Analysis')).toBeInTheDocument());

    expect(screen.getByText('0.886 kg')).toBeInTheDocument();
    expect(screen.getByText('300')).toBeInTheDocument();
    expect(screen.getByText('carbon-fiber')).toBeInTheDocument();
  });
});
