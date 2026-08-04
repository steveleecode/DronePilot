export type Vector3 = {
  x: number;
  y: number;
  z: number;
};

export type Material = {
  id: string;
  name: string;
  density_kg_m3: number;
  source_note: string;
};

export type AnalyzedPart = {
  id: string;
  name: string;
  volume_m3: number;
  surface_area_m2: number | null;
  center_of_mass_m: Vector3;
  source_type: 'solid' | 'compound' | 'assembly_component';
  warnings: string[];
  material_id: string | null;
  density_kg_m3: number | null;
  mass_kg: number;
  mass_source: 'density_calculated' | 'manufacturer_override' | 'unassigned';
  inertia_tensor_kg_m2: number[][];
};

export type DroneAnalysis = {
  model_id: string;
  part_count: number;
  total_volume_m3: number;
  total_mass_kg: number;
  center_of_gravity_m: Vector3;
  inertia_tensor_kg_m2: number[][];
  principal_moments_kg_m2: number[];
  bounding_box_m: Vector3;
  materials: Material[];
  parts: AnalyzedPart[];
  warnings: string[];
  metadata: {
    source_step_path: string;
    source_length_unit: string;
    coordinate_convention: string;
    unit_convention: string;
    processing_version: string;
    default_material_id: string | null;
  };
};

export type DroneModelMetadata = {
  model_id: string;
  source_step_path: string;
  analysis_url: string;
  geometry_url: string;
};
