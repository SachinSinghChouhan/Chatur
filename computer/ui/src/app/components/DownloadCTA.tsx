import { useRef } from 'react';
import { motion, useInView } from 'motion/react';
import { Download, Shield, Code, Layers } from 'lucide-react';

const highlights = [
  { icon: Shield, text: 'Privacy-first design' },
  { icon: Code, text: 'Fully open source' },
  { icon: Layers, text: 'No cloud dependency' },
];

export function DownloadCTA() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.2 });

  return (
    <section
      ref={ref}
      className="py-32 px-6"
      style={{
        background: 'linear-gradient(180deg, var(--background) 0%, var(--background-secondary) 100%)',
      }}
    >
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <h2 className="text-4xl md:text-5xl mb-6" style={{ color: 'var(--text-primary)' }}>
            Ready to Get Started?
          </h2>
          <p className="text-lg mb-8" style={{ color: 'var(--text-secondary)' }}>
            Download Chatur and experience voice control designed for you
          </p>

          {/* Requirements */}
          <div className="mb-10">
            <p className="text-sm" style={{ color: 'var(--text-muted)' }}>
              Requirements: Windows 10/11 or Ubuntu 20.04+ • 4GB RAM • Microphone
            </p>
          </div>

          {/* Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <a
              href="https://github.com/SachinSinghChouhan/Chatur/releases/latest/download/ChaturAssistant-windows-x64.exe"
              className="px-8 py-4 rounded-lg flex items-center gap-2 transition-all duration-200 hover:bg-[var(--accent-primary)] hover:border-[var(--accent-primary)] group shadow-lg hover:shadow-[0_0_20px_rgba(99,102,241,0.5)] bg-black"
              style={{
                color: 'var(--text-primary)',
                border: '1px solid var(--surface-border)',
                textDecoration: 'none',
              }}
            >
              <Download className="w-5 h-5" />
              Download for Windows
            </a>
            <a
              href="https://github.com/SachinSinghChouhan/Chatur/releases/latest/download/ChaturAssistant-linux-x64"
              className="px-8 py-4 rounded-lg flex items-center gap-2 transition-all duration-200 hover:bg-[var(--accent-primary)] hover:border-[var(--accent-primary)] group shadow-lg hover:shadow-[0_0_20px_rgba(99,102,241,0.5)] bg-black"
              style={{
                color: 'var(--text-primary)',
                border: '1px solid var(--surface-border)',
                textDecoration: 'none',
              }}
            >
              <Download className="w-5 h-5" />
              Download for Ubuntu
            </a>
          </div>

          {/* Highlights */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
            {highlights.map((highlight, index) => (
              <motion.div
                key={highlight.text}
                initial={{ opacity: 0, y: 10 }}
                animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 10 }}
                transition={{ duration: 0.5, delay: 0.2 + index * 0.1, ease: 'easeOut' }}
                className="flex items-center gap-2"
              >
                <highlight.icon className="w-4 h-4" style={{ color: 'var(--accent-primary)' }} />
                <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                  {highlight.text}
                </span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}