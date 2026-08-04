import { formatLengthM, formatMassKg, formatTensorValue, formatVolumeM3 } from '../../lib/format';
import type { DroneAnalysis, Vector3 } from '../../lib/types';

type Props = {
  analysis: DroneAnalysis;
};

function vectorText(vector: Vector3): string {
  return `x ${formatLengthM(vector.x)}, y ${formatLengthM(vector.y)}, z ${formatLengthM(vector.z)}`;
}

export function EngineeringPanel({ analysis }: Props) {
  return (
    <aside className="property-panel" aria-label="Engineering properties">
      <header>
        <p>{analysis.model_id}</p>
        <h1>CAD Analysis</h1>
      </header>

      <dl className="metric-grid">
        <div>
          <dt>Total mass</dt>
          <dd>{formatMassKg(analysis.total_mass_kg)}</dd>
        </div>
        <div>
          <dt>Total volume</dt>
          <dd>{formatVolumeM3(analysis.total_volume_m3)}</dd>
        </div>
        <div>
          <dt>Parts</dt>
          <dd>{analysis.part_count}</dd>
        </div>
        <div>
          <dt>Default material</dt>
          <dd>{analysis.metadata.default_material_id ?? 'None'}</dd>
        </div>
      </dl>

      <section>
        <h2>Bounds</h2>
        <p>{vectorText(analysis.bounding_box_m)}</p>
      </section>

      <section>
        <h2>Center of Gravity</h2>
        <p>{vectorText(analysis.center_of_gravity_m)}</p>
      </section>

      <section>
        <h2>Inertia Tensor</h2>
        <table>
          <tbody>
            {analysis.inertia_tensor_kg_m2.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((value, columnIndex) => (
                  <td key={`${rowIndex}-${columnIndex}`}>{formatTensorValue(value)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {analysis.warnings.length > 0 ? (
        <section>
          <h2>Warnings</h2>
          <ul>
            {analysis.warnings.map((warning) => (
              <li key={warning}>{warning}</li>
            ))}
          </ul>
        </section>
      ) : null}
    </aside>
  );
}
