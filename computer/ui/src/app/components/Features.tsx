import React, { useRef } from 'react';
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

export function Features() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.1 });

  return (
    <section ref={ref} className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl mb-4" style={{ color: 'var(--text-primary)' }}>
            Features
          </h2>
          <p className="text-lg" style={{ color: 'var(--text-secondary)' }}>
            Powerful capabilities designed for seamless voice interaction
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
              transition={{ duration: 0.5, delay: index * 0.1, ease: 'easeOut' }}
              className="p-6 rounded-lg border transition-all duration-200 hover:-translate-y-1"
              style={{
                backgroundColor: 'var(--surface-card)',
                borderColor: 'var(--surface-border)',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
              }}
            >
              <div
                className="w-12 h-12 rounded-lg flex items-center justify-center mb-4"
                style={{ backgroundColor: 'rgba(100, 116, 139, 0.1)' }}
              >
                <feature.icon className="w-6 h-6" style={{ color: 'var(--accent-primary)' }} />
              </div>

              <h3 className="mb-2" style={{ color: 'var(--text-primary)' }}>
                {feature.title}
              </h3>

              <p className="text-sm" style={{ color: 'var(--text-muted)' }}>
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}