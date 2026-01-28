import React, { useRef, useState } from 'react';
import { motion, useInView } from 'motion/react';
import {
  Layers,
  Shield,
  Globe,
  Code,
  Boxes,
  Workflow,
} from 'lucide-react';

const features = [
  {
    icon: Globe,
    title: 'Bilingual Support',
    description: 'Seamlessly switch between English and Hindi. Understands Hinglish naturally.',
  },
  {
    icon: Shield,
    title: 'Privacy First',
    description: 'All processing happens locally on your machine. No data sent to the cloud.',
  },
  {
    icon: Layers,
    title: 'Context Aware',
    description: 'Remembers conversation context and adapts to your speech patterns over time.',
  },
  {
    icon: Workflow,
    title: 'Task Automation',
    description: 'Control applications, files, and system settings with simple voice commands.',
  },
  {
    icon: Code,
    title: 'Open Source',
    description: 'Fully transparent codebase. Contribute, customize, and extend functionality.',
  },
  {
    icon: Boxes,
    title: 'Extensible Plugins',
    description: 'Add custom skills and integrations through a simple plugin architecture.',
  },
];

const FeatureCard = ({ feature, index }: { feature: any; index: number }) => {
  const divRef = useRef<HTMLDivElement>(null);
  const [isFocused, setIsFocused] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [opacity, setOpacity] = useState(0);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!divRef.current) return;

    const div = divRef.current;
    const rect = div.getBoundingClientRect();

    setPosition({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  };

  const handleFocus = () => {
    setIsFocused(true);
    setOpacity(1);
  };

  const handleBlur = () => {
    setIsFocused(false);
    setOpacity(0);
  };

  const handleMouseEnter = () => {
    setOpacity(1);
  };

  const handleMouseLeave = () => {
    setOpacity(0);
  };

  return (
    <motion.div
      ref={divRef}
      onMouseMove={handleMouseMove}
      onFocus={handleFocus}
      onBlur={handleBlur}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay: index * 0.1, ease: 'easeOut' }}
      className="relative p-8 rounded-2xl border overflow-hidden group h-full"
      style={{
        backgroundColor: 'rgba(255, 255, 255, 0.03)',
        borderColor: 'var(--surface-border)',
      }}
    >
      {/* Spotlight Gradient */}
      <div
        className="pointer-events-none absolute -inset-px opacity-0 transition duration-300"
        style={{
          opacity,
          background: `radial-gradient(600px circle at ${position.x}px ${position.y}px, rgba(255,255,255,0.06), transparent 40%)`,
        }}
      />

      {/* Content */}
      <div className="relative z-10">
        <div
          className="w-14 h-14 rounded-xl flex items-center justify-center mb-6 transition-colors duration-300 group-hover:bg-[var(--accent-primary)] group-hover:text-white"
          style={{
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            color: 'var(--accent-primary)'
          }}
        >
          <feature.icon className="w-7 h-7" />
        </div>

        <h3 className="mb-3 text-xl font-semibold" style={{ color: 'var(--text-primary)' }}>
          {feature.title}
        </h3>

        <p className="text-sm leading-relaxed" style={{ color: 'var(--text-muted)' }}>
          {feature.description}
        </p>
      </div>
    </motion.div>
  );
};

export function Features() {
  const ref = useRef(null);

  return (
    <section ref={ref} className="py-24 px-6 relative overflow-hidden">
      {/* Ambient background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-indigo-500/5 rounded-full blur-[100px] pointer-events-none" />

      <div className="max-w-6xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl md:text-5xl mb-4 font-bold tracking-tight"
            style={{ color: 'var(--text-primary)' }}
          >
            Capabilities
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-lg"
            style={{ color: 'var(--text-secondary)' }}
          >
            Engineered for performance and privacy
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <FeatureCard key={feature.title} feature={feature} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
}