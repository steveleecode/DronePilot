import { OrbitControls, PerspectiveCamera, useGLTF } from '@react-three/drei';
import { Canvas, useThree } from '@react-three/fiber';
import { Suspense, useEffect, useMemo } from 'react';
import type { Group, Mesh } from 'three';
import { Color, MeshBasicMaterial } from 'three';

import { resolveApiUrl } from '../../lib/api';
import type { DroneAnalysis } from '../../lib/types';

type Props = {
  analysis: DroneAnalysis;
  modelUrl: string;
  showCog: boolean;
  wireframe: boolean;
  resetToken: number;
};

export function DroneScene({ analysis, modelUrl, showCog, wireframe, resetToken }: Props) {
  return (
    <Canvas className="canvas" shadows>
      <color attach="background" args={['#eef2ea']} />
      <PerspectiveCamera makeDefault position={[1.12, -1.46, 0.62]} fov={56} />
      <ZUpCamera resetToken={resetToken} />
      <hemisphereLight args={['#ffffff', '#c9d3c8', 1.45]} />
      <directionalLight position={[1.5, -2.5, 3]} intensity={2.6} />
      <directionalLight position={[-2, 2, 2]} intensity={0.9} />
      <Suspense fallback={null}>
        <DroneModel url={resolveApiUrl(modelUrl)} wireframe={wireframe} />
        {showCog ? <CogMarker analysis={analysis} /> : null}
      </Suspense>
      <gridHelper args={[0.7, 14, '#9aa89f', '#c6d0c8']} rotation={[Math.PI / 2, 0, 0]} />
      <axesHelper args={[0.18]} />
      <OrbitControls makeDefault enableDamping dampingFactor={0.08} />
    </Canvas>
  );
}

function ZUpCamera({ resetToken }: { resetToken: number }) {
  const { camera, controls } = useThree();

  useEffect(() => {
    const orbitControls = controls as unknown as
      | {
          target: { set: (x: number, y: number, z: number) => void };
          update: () => void;
        }
      | undefined;
    camera.up.set(0, 0, 1);
    camera.position.set(1.12, -1.46, 0.62);
    camera.lookAt(-0.23, 0.0, -0.04);
    orbitControls?.target.set(-0.23, 0.0, -0.04);
    orbitControls?.update();
  }, [camera, controls, resetToken]);

  return null;
}

function DroneModel({ url, wireframe }: { url: string; wireframe: boolean }) {
  const gltf = useGLTF(url);
  const scene = useMemo(() => gltf.scene.clone(true), [gltf.scene]);

  useEffect(() => {
    scene.traverse((object) => {
      const mesh = object as Mesh;
      if (mesh.isMesh) {
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        mesh.material = new MeshBasicMaterial({
          color: new Color(wireframe ? '#27473d' : '#6f8d80'),
          wireframe,
        });
      }
    });
  }, [scene, wireframe]);

  return <primitive object={scene as Group} />;
}

function CogMarker({ analysis }: { analysis: DroneAnalysis }) {
  const cog = analysis.center_of_gravity_m;

  return (
    <group position={[cog.x, cog.y, cog.z]}>
      <mesh>
        <sphereGeometry args={[0.012, 24, 16]} />
        <meshStandardMaterial color="#d94b35" emissive="#6d140b" emissiveIntensity={0.2} />
      </mesh>
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <ringGeometry args={[0.018, 0.021, 32]} />
        <meshBasicMaterial color="#d94b35" />
      </mesh>
    </group>
  );
}
