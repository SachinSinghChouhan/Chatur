import { useRef } from 'react';
import { motion, useInView } from 'motion/react';
import { Terminal } from 'lucide-react';

const techStack = [
  'Python',
  'PyTorch',
  'Whisper',
  'spaCy',
  'Windows API',
  'gTTS',
];

export function DeveloperSection() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.2 });

  return (
    <section ref={ref} className="py-24 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl mb-4" style={{ color: 'var(--text-primary)' }}>
            Built for Developers
          </h2>
          <p className="text-lg" style={{ color: 'var(--text-secondary)' }}>
            Easy to install, customize, and extend
          </p>
        </motion.div>

        {/* Terminal Block */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.5, delay: 0.2, ease: 'easeOut' }}
          className="rounded-lg border overflow-hidden"
          style={{
            backgroundColor: '#1a1d28',
            borderColor: 'var(--surface-border)',
          }}
        >
          {/* Terminal Header */}
          <div
            className="px-4 py-3 flex items-center gap-2 border-b"
            style={{ borderColor: 'var(--surface-border)' }}
          >
            <Terminal className="w-4 h-4" style={{ color: 'var(--text-muted)' }} />
            <span className="text-sm" style={{ color: 'var(--text-muted)' }}>
              Quick Start
            </span>
          </div>

          {/* Terminal Content */}
          <div className="p-6 font-mono text-sm">
            <div className="mb-4">
              <span style={{ color: 'var(--text-muted)' }}># Clone the repository</span>
            </div>
            <div className="mb-4">
              <span style={{ color: '#7dd3fc' }}>git clone</span>{' '}
              <span style={{ color: 'var(--text-secondary)' }}>
                https://github.com/yourusername/chatur.git
              </span>
            </div>

            <div className="mb-4 mt-6">
              <span style={{ color: 'var(--text-muted)' }}># Install dependencies</span>
            </div>
            <div className="mb-4">
              <span style={{ color: '#7dd3fc' }}>cd</span>{' '}
              <span style={{ color: 'var(--text-secondary)' }}>chatur</span>
            </div>
            <div className="mb-4">
              <span style={{ color: '#7dd3fc' }}>pip install</span>{' '}
              <span style={{ color: '#a78bfa' }}>-r</span>{' '}
              <span style={{ color: 'var(--text-secondary)' }}>requirements.txt</span>
            </div>

            <div className="mb-4 mt-6">
              <span style={{ color: 'var(--text-muted)' }}># Run Chatur</span>
            </div>
            <div>
              <span style={{ color: '#7dd3fc' }}>python</span>{' '}
              <span style={{ color: 'var(--text-secondary)' }}>chatur.py</span>
            </div>
          </div>
        </motion.div>

        {/* Tech Stack */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.5, delay: 0.4, ease: 'easeOut' }}
          className="mt-12 text-center"
        >
          <p className="text-sm mb-4" style={{ color: 'var(--text-muted)' }}>
            Built with modern technologies
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            {techStack.map((tech) => (
              <span
                key={tech}
                className="px-4 py-2 rounded-md text-sm border"
                style={{
                  backgroundColor: 'var(--surface-card)',
                  borderColor: 'var(--surface-border)',
                  color: 'var(--text-secondary)',
                }}
              >
                {tech}
              </span>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}