import React, { useEffect, useRef } from 'react';

const StatusDot = ({ active, color, label }) => (
  <div
    className={`w-2 h-2 rounded-full ${active ? color : 'bg-gray-600'}`}
    title={label}
  />
);

const TopAudioBar = ({
  audioData,
  isBackendConnected = false,
  isOrionRunning = false,
  isCameraActive = false,
  isPrinterConnected = false,
}) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const draw = () => {
      const width = canvas.width;
      const height = canvas.height;
      ctx.clearRect(0, 0, width, height);

      const barWidth = 4;
      const gap = 2;
      const totalBars = Math.floor(width / (barWidth + gap));
      const center = width / 2;

      for (let i = 0; i < totalBars / 2; i++) {
        const value = audioData[i % audioData.length] || 0;
        const percent = value / 255;
        const barHeight = Math.max(2, percent * height);

        ctx.fillStyle = `rgba(34, 211, 238, ${0.2 + percent * 0.8})`;

        ctx.fillRect(center + i * (barWidth + gap), (height - barHeight) / 2, barWidth, barHeight);
        ctx.fillRect(center - (i + 1) * (barWidth + gap), (height - barHeight) / 2, barWidth, barHeight);
      }
    };

    requestAnimationFrame(draw);
  }, [audioData]);

  return (
    <div className="flex flex-col items-center gap-1">
      <canvas ref={canvasRef} width={300} height={40} className="opacity-80" />
      <div className="flex gap-2">
        <StatusDot active={isBackendConnected} color="bg-green-500" label="Backend" />
        <StatusDot active={isOrionRunning} color="bg-cyan-400" label="ORION" />
        <StatusDot active={isCameraActive} color="bg-blue-400" label="Camera" />
        <StatusDot active={isPrinterConnected} color="bg-purple-400" label="Printer" />
      </div>
    </div>
  );
};

export default TopAudioBar;
