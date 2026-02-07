
import React, { useEffect, useRef } from 'react';

/**
 * REFINED MEDICAL BACKGROUND
 * - Continuous high-fidelity ECG waveform
 * - Dynamic data-node particle system (Canvas)
 * - Layered opacity for depth (4-12%)
 */

const MedicalBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let nodes: Array<{ x: number; y: number; vx: number; vy: number; r: number; opacity: number }> = [];

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initNodes();
    };

    const initNodes = () => {
      nodes = Array.from({ length: 35 }, () => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 2 + 1,
        opacity: Math.random() * 0.12 + 0.04,
      }));
    };

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      nodes.forEach((node, i) => {
        // Move nodes
        node.x += node.vx;
        node.y += node.vy;

        // Wrap around
        if (node.x < 0) node.x = canvas.width;
        if (node.x > canvas.width) node.x = 0;
        if (node.y < 0) node.y = canvas.height;
        if (node.y > canvas.height) node.y = 0;

        // Draw node
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 255, 255, ${node.opacity})`;
        ctx.fill();

        // Connect nodes near each other
        for (let j = i + 1; j < nodes.length; j++) {
          const other = nodes[j];
          const dx = node.x - other.x;
          const dy = node.y - other.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 150) {
            ctx.beginPath();
            ctx.strokeStyle = `rgba(0, 255, 255, ${(1 - dist / 150) * 0.05})`;
            ctx.lineWidth = 0.5;
            ctx.moveTo(node.x, node.y);
            ctx.lineTo(other.x, other.y);
            ctx.stroke();
          }
        }
      });

      animationFrameId = requestAnimationFrame(draw);
    };

    window.addEventListener('resize', resize);
    resize();
    draw();

    return () => {
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  // Complex ECG Path definition
  const ecgPath = "M0,100 L80,100 L90,85 L100,115 L110,40 L120,160 L130,100 L200,100 L210,95 L220,105 L230,100 L300,100 L310,85 L320,115 L330,40 L340,160 L350,100 L420,100 L430,95 L440,105 L450,100 L500,100";

  return (
    <div className="medical-background">
      {/* Background Vignette / Depth */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,_transparent_0%,_rgba(2,6,23,0.8)_100%)]" />
      
      {/* Layer 1: The Grid */}
      <div className="medical-grid" />
      
      {/* Layer 2: Scrolling ECG Line */}
      <div className="ecg-layer">
        <svg width="100%" height="200" viewBox="0 0 500 200" preserveAspectRatio="none" className="w-full">
          <path
            d={ecgPath}
            fill="none"
            stroke="rgba(0, 255, 255, 0.8)"
            strokeWidth="1.5"
            vectorEffect="non-scaling-stroke"
          />
          {/* Animated Glow Dot following the "lead" */}
          <circle r="2" fill="cyan">
            <animateMotion dur="4s" repeatCount="indefinite" path={ecgPath} />
          </circle>
        </svg>
        <svg width="100%" height="200" viewBox="0 0 500 200" preserveAspectRatio="none" className="w-full">
          <path
            d={ecgPath}
            fill="none"
            stroke="rgba(0, 255, 255, 0.8)"
            strokeWidth="1.5"
            vectorEffect="non-scaling-stroke"
          />
          <circle r="2" fill="cyan">
            <animateMotion dur="4s" repeatCount="indefinite" path={ecgPath} />
          </circle>
        </svg>
      </div>

      {/* Layer 3: Data Network Particles */}
      <canvas ref={canvasRef} className="absolute inset-0" />

      {/* Layer 4: Floating Scan Line */}
      <div className="scan-line" />
    </div>
  );
};

export default MedicalBackground;
