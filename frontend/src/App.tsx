import { useEffect, useState } from 'react';
import { AlertTriangle, Loader2 } from './components/Icons';
import { EngineeringPanel } from './features/analysis/EngineeringPanel';
import { DroneScene } from './features/viewer/DroneScene';
import { fetchDroneAnalysis, fetchDroneModel } from './lib/api';
import type { DroneAnalysis, DroneModelMetadata } from './lib/types';

type LoadState =
  | { status: 'loading' }
  | { status: 'ready'; model: DroneModelMetadata; analysis: DroneAnalysis }
  | { status: 'error'; message: string };

export function App() {
  const [state, setState] = useState<LoadState>({ status: 'loading' });
  const [showCog, setShowCog] = useState(true);
  const [wireframe, setWireframe] = useState(false);
  const [resetToken, setResetToken] = useState(0);

  useEffect(() => {
    let active = true;

    async function load() {
      try {
        const [model, analysis] = await Promise.all([fetchDroneModel(), fetchDroneAnalysis()]);
        if (active) {
          setState({ status: 'ready', model, analysis });
        }
      } catch (error) {
        if (active) {
          setState({
            status: 'error',
            message: error instanceof Error ? error.message : 'Unable to load drone data.',
          });
        }
      }
    }

    void load();
    return () => {
      active = false;
    };
  }, []);

  if (state.status === 'loading') {
    return (
      <main className="app-shell status-shell">
        <Loader2 className="spin" />
        <span>Loading drone model</span>
      </main>
    );
  }

  if (state.status === 'error') {
    return (
      <main className="app-shell status-shell error">
        <AlertTriangle />
        <span>{state.message}</span>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <section className="viewer-region" aria-label="Interactive drone CAD viewer">
        <DroneScene
          analysis={state.analysis}
          modelUrl={state.model.geometry_url}
          showCog={showCog}
          wireframe={wireframe}
          resetToken={resetToken}
        />
        <div className="viewer-toolbar" aria-label="Viewer controls">
          <button type="button" onClick={() => setResetToken((value) => value + 1)}>
            Reset
          </button>
          <label>
            <input
              type="checkbox"
              checked={showCog}
              onChange={(event) => setShowCog(event.currentTarget.checked)}
            />
            COG
          </label>
          <label>
            <input
              type="checkbox"
              checked={wireframe}
              onChange={(event) => setWireframe(event.currentTarget.checked)}
            />
            Wire
          </label>
        </div>
      </section>
      <EngineeringPanel analysis={state.analysis} />
    </main>
  );
}
