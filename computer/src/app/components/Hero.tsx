import React from 'react';
import { motion } from 'motion/react';
import { Mic, Github, Download } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 py-20 pt-32">
      <div className="max-w-4xl mx-auto text-center">
        {/* Microphone Icon with Subtle Pulse */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="mb-12 flex justify-center"
        >
          <div className="relative">
            <motion.div
              animate={{ scale: [1, 1.02, 1] }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
              className="w-24 h-24 rounded-full bg-[var(--surface-card)] border border-[var(--surface-border)] flex items-center justify-center"
            >
              <Mic className="w-10 h-10 text-[var(--accent-primary)]" />
            </motion.div>
            {/* Subtle outer ring */}
            <motion.div
              animate={{ scale: [1, 1.1, 1], opacity: [0.3, 0.1, 0.3] }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
              className="absolute inset-0 rounded-full border border-[var(--accent-primary)] opacity-20"
            />
          </div>
        </motion.div>

        {/* Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: 'easeOut' }}
          className="text-5xl md:text-6xl lg:text-7xl mb-6 tracking-tight"
          style={{ color: 'var(--text-primary)' }}
        >
          Meet Chatur
        </motion.h1>

        {/* Subheading */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3, ease: 'easeOut' }}
          className="text-xl md:text-2xl mb-12 max-w-2xl mx-auto"
          style={{ color: 'var(--text-secondary)' }}
        >
          A bilingual personal voice assistant for Windows.
          <br />
          Speak naturally in English or Hindi.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4, ease: 'easeOut' }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <button
            className="px-8 py-4 rounded-lg flex items-center gap-2 transition-all duration-200 hover:opacity-90"
            style={{
              backgroundColor: 'var(--accent-primary)',
              color: 'var(--text-primary)',
            }}
          >
            <Download className="w-5 h-5" />
            Download for Windows
          </button>
          <button
            className="px-8 py-4 rounded-lg flex items-center gap-2 border transition-all duration-200 hover:bg-[var(--surface-card)]"
            style={{
              borderColor: 'var(--surface-border)',
              color: 'var(--text-secondary)',
            }}
          >
            <Github className="w-5 h-5" />
            View on GitHub
          </button>
        </motion.div>

        {/* Version info */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.6, ease: 'easeOut' }}
          className="mt-8 text-sm"
          style={{ color: 'var(--text-muted)' }}
        >
          Open source • Privacy-first • Local processing
        </motion.p>
      </div>
    </section>
  );
}