import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import AILoader from '../AILoader/AILoader';
import styles from '../AILoader/AILoader.module.css';

/**
 * HeroRobot - Exact video reference match
 *
 * VIDEO IS THE ONLY SOURCE OF TRUTH
 */
export default function HeroRobot() {
  const containerRef = useRef(null);
  const [isClient, setIsClient] = useState(false);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (!isClient || !containerRef.current) return;

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    const scene = new THREE.Scene();

    // Camera - VIDEO MATCH: Human eye-level, slight top-down, static
    const camera = new THREE.PerspectiveCamera(36, width / height, 0.1, 100);
    camera.position.set(0, 1.5, 4.8);
    camera.lookAt(0, 0.25, 0);

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 0.95;
    container.appendChild(renderer.domElement);

    // Materials - Black robot with cyan accents
    const robotMaterial = new THREE.MeshStandardMaterial({
      color: 0x080808,
      metalness: 0.88,
      roughness: 0.22,
    });

    const accentMaterial = new THREE.MeshStandardMaterial({
      color: 0x00b4d8,
      emissive: 0x00b4d8,
      emissiveIntensity: 0.35,
      metalness: 0.55,
      roughness: 0.18,
    });

    const eyeMaterial = new THREE.MeshStandardMaterial({
      color: 0x00ffff,
      emissive: 0x00ffff,
      emissiveIntensity: 1.2,
    });

    // Robot group
    const robotGroup = new THREE.Group();
    robotGroup.position.set(0, -1.15, 0);

    // Head
    const head = new THREE.Mesh(
      new THREE.CapsuleGeometry(0.165, 0.19, 8, 16),
      robotMaterial
    );
    head.position.y = 1.58;
    robotGroup.add(head);

    // Face
    const face = new THREE.Mesh(
      new THREE.BoxGeometry(0.25, 0.155, 0.038),
      robotMaterial
    );
    face.position.set(0, 1.6, 0.095);
    robotGroup.add(face);

    // Eyes
    const leftEye = new THREE.Mesh(
      new THREE.SphereGeometry(0.021, 16, 16),
      eyeMaterial
    );
    leftEye.position.set(-0.068, 1.62, 0.125);
    robotGroup.add(leftEye);

    const rightEye = new THREE.Mesh(
      new THREE.SphereGeometry(0.021, 16, 16),
      eyeMaterial
    );
    rightEye.position.set(0.068, 1.62, 0.125);
    robotGroup.add(rightEye);

    // Eye accents
    const leftAccent = new THREE.Mesh(
      new THREE.BoxGeometry(0.048, 0.014, 0.0048),
      accentMaterial
    );
    leftAccent.position.set(-0.068, 1.62, 0.13);
    robotGroup.add(leftAccent);

    const rightAccent = new THREE.Mesh(
      new THREE.BoxGeometry(0.048, 0.014, 0.0048),
      accentMaterial
    );
    rightAccent.position.set(0.068, 1.62, 0.13);
    robotGroup.add(rightAccent);

    // Antenna
    const antenna = new THREE.Mesh(
      new THREE.CylinderGeometry(0.011, 0.011, 0.095, 8),
      robotMaterial
    );
    antenna.position.set(0, 1.79, 0);
    robotGroup.add(antenna);

    const antennaTop = new THREE.Mesh(
      new THREE.SphereGeometry(0.019, 12, 12),
      accentMaterial
    );
    antennaTop.position.set(0, 1.845, 0);
    robotGroup.add(antennaTop);

    // Neck
    const neck = new THREE.Mesh(
      new THREE.CylinderGeometry(0.053, 0.062, 0.075, 16),
      robotMaterial
    );
    neck.position.y = 1.35;
    robotGroup.add(neck);

    // Torso
    const torso = new THREE.Mesh(
      new THREE.CylinderGeometry(0.175, 0.135, 0.68, 16),
      robotMaterial
    );
    torso.position.y = 0.92;
    robotGroup.add(torso);

    // Chest
    const chest = new THREE.Mesh(
      new THREE.BoxGeometry(0.27, 0.215, 0.058),
      robotMaterial
    );
    chest.position.set(0, 1.05, 0.075);
    robotGroup.add(chest);

    // Core
    const core = new THREE.Mesh(
      new THREE.CircleGeometry(0.048, 24),
      accentMaterial
    );
    core.position.set(0, 1.05, 0.115);
    robotGroup.add(core);

    // Waist
    const waist = new THREE.Mesh(
      new THREE.CylinderGeometry(0.095, 0.095, 0.115, 16),
      robotMaterial
    );
    waist.position.y = 0.53;
    robotGroup.add(waist);

    // Arms
    const createArm = (side) => {
      const armGroup = new THREE.Group();
      const sign = side === 'left' ? -1 : 1;

      const shoulder = new THREE.Mesh(
        new THREE.SphereGeometry(0.068, 12, 12),
        robotMaterial
      );
      armGroup.add(shoulder);

      const upperArm = new THREE.Mesh(
        new THREE.CapsuleGeometry(0.043, 0.175, 6, 8),
        robotMaterial
      );
      upperArm.position.y = -0.135;
      armGroup.add(upperArm);

      const elbow = new THREE.Mesh(
        new THREE.SphereGeometry(0.053, 12, 12),
        robotMaterial
      );
      elbow.position.y = -0.31;
      armGroup.add(elbow);

      const forearm = new THREE.Mesh(
        new THREE.CapsuleGeometry(0.034, 0.213, 6, 8),
        robotMaterial
      );
      forearm.position.y = -0.485;
      armGroup.add(forearm);

      const hand = new THREE.Mesh(
        new THREE.BoxGeometry(0.053, 0.068, 0.034),
        robotMaterial
      );
      hand.position.y = -0.64;
      armGroup.add(hand);

      armGroup.position.x = sign * 0.253;
      armGroup.position.y = 1.22;

      return armGroup;
    };

    const leftArm = createArm('left');
    const rightArm = createArm('right');
    robotGroup.add(leftArm);
    robotGroup.add(rightArm);

    // Hips
    const hips = new THREE.Mesh(
      new THREE.SphereGeometry(0.116, 12, 12),
      robotMaterial
    );
    hips.position.y = 0.37;
    robotGroup.add(hips);

    // Legs
    const createLeg = (side) => {
      const legGroup = new THREE.Group();
      const sign = side === 'left' ? -1 : 1;

      const upperLeg = new THREE.Mesh(
        new THREE.CapsuleGeometry(0.058, 0.31, 6, 8),
        robotMaterial
      );
      upperLeg.position.y = -0.272;
      legGroup.add(upperLeg);

      const knee = new THREE.Mesh(
        new THREE.SphereGeometry(0.058, 12, 12),
        robotMaterial
      );
      knee.position.y = -0.505;
      legGroup.add(knee);

      const lowerLeg = new THREE.Mesh(
        new THREE.CapsuleGeometry(0.043, 0.34, 6, 8),
        robotMaterial
      );
      lowerLeg.position.y = -0.755;
      legGroup.add(lowerLeg);

      const foot = new THREE.Mesh(
        new THREE.BoxGeometry(0.087, 0.043, 0.126),
        robotMaterial
      );
      foot.position.set(0.014, -1.05, 0.038);
      legGroup.add(foot);

      legGroup.position.x = sign * 0.097;
      legGroup.position.y = 0.097;

      return legGroup;
    };

    const leftLeg = createLeg('left');
    const rightLeg = createLeg('right');
    robotGroup.add(leftLeg);
    robotGroup.add(rightLeg);

    robotGroup.scale.set(0.95, 0.95, 0.95);
    scene.add(robotGroup);

    // Lighting - VIDEO MATCH: Studio soft lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.38);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xfff9f0, 0.85);
    keyLight.position.set(3.5, 5.5, 2.5);
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0xeaf2ff, 0.32);
    fillLight.position.set(-3.5, 2.5, 1.5);
    scene.add(fillLight);

    const rimLight = new THREE.SpotLight(0x00b4d8, 0.55);
    rimLight.position.set(-1.5, 3.5, -2.5);
    rimLight.angle = 0.65;
    rimLight.penumbra = 1;
    scene.add(rimLight);

    const backLight = new THREE.SpotLight(0x4a90d9, 0.25);
    backLight.position.set(1.5, 2.5, -2.5);
    backLight.angle = 0.55;
    backLight.penumbra = 1;
    scene.add(backLight);

    // Shadow
    const shadowGeometry = new THREE.CircleGeometry(1.15, 32);
    const shadowMaterial = new THREE.MeshBasicMaterial({
      color: 0x000000,
      transparent: true,
      opacity: 0.2,
    });
    const shadow = new THREE.Mesh(shadowGeometry, shadowMaterial);
    shadow.rotation.x = -Math.PI / 2;
    shadow.position.y = -1.12;
    scene.add(shadow);

    // Animation - VIDEO MATCH: Extremely slow, almost imperceptible
    let mouseX = 0;
    let mouseY = 0;
    let currentRotationY = 0;
    let currentRotationX = 0;
    let currentPosY = 0;
    let idleTime = 0;
    let frameCount = 0;

    const handleMouseMove = (event) => {
      const rect = container.getBoundingClientRect();
      mouseX = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouseY = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    };

    container.addEventListener('mousemove', handleMouseMove);

    const clock = new THREE.Clock();

    const animate = () => {
      idleTime += clock.getDelta();

      // FLOATING - Extremely slow, almost imperceptible
      const floatY = Math.sin(idleTime * 0.5) * 0.04;
      currentPosY = THREE.MathUtils.lerp(currentPosY, floatY, 0.02);
      robotGroup.position.y = -1.15 + currentPosY;

      // BREATHING - Nearly invisible
      const breathe = 1 + Math.sin(idleTime * 0.35) * 0.003;
      torso.scale.y = breathe;

      // IDLE ROTATION - Almost none, very subtle sway
      const idleRotation = Math.sin(idleTime * 0.25) * 0.04;

      // MOUSE PARALLAX - Barely noticeable
      const targetRotY = mouseX * 0.04;
      const targetRotX = mouseY * 0.02;

      currentRotationY = THREE.MathUtils.lerp(currentRotationY, idleRotation + targetRotY, 0.02);
      currentRotationX = THREE.MathUtils.lerp(currentRotationX, targetRotX, 0.03);

      robotGroup.rotation.y = currentRotationY;
      robotGroup.rotation.x = currentRotationX;

      // ARM SWAY - Minimal
      leftArm.rotation.z = Math.sin(idleTime * 0.3) * 0.015;
      rightArm.rotation.z = -Math.sin(idleTime * 0.3) * 0.015;

      renderer.render(scene, camera);

      // Signal ready after a few frames to ensure clean render
      if (frameCount < 10) {
        frameCount++;
        if (frameCount === 5) {
          setIsReady(true);
        }
      }

      requestAnimationFrame(animate);
    };

    animate();

    const handleResize = () => {
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      container.removeEventListener('mousemove', handleMouseMove);
      container.removeChild(renderer.domElement);
      renderer.dispose();
    };
  }, [isClient]);

  // SSR fallback - Static for mobile
  if (!isClient) {
    return (
      <div
        className="hero-robot-container"
        style={{
          width: '100%',
          height: '100%',
          minHeight: '450px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #0a0c1e 0%, #0f1228 50%, #1a1f3a 100%)',
        }}
      >
        <AILoader isVisible={true} />
      </div>
    );
  }

  return (
    <div
      style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        minHeight: '450px',
        overflow: 'hidden'
      }}
    >
      <div
        className={`${styles.loaderContainer} ${isReady ? styles.loaderHidden : ''}`}
      >
        <AILoader isVisible={true} />
      </div>

      <div
        ref={containerRef}
        className="hero-robot-container"
        style={{
          width: '100%',
          height: '100%',
          transition: 'opacity 1s cubic-bezier(0.4, 0, 0.2, 1), transform 1.2s cubic-bezier(0.4, 0, 0.2, 1)',
          opacity: isReady ? 1 : 0,
          transform: isReady ? 'scale(1)' : 'scale(1.1)',
        }}
      />
    </div>
  );
}

