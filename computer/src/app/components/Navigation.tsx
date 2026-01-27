import React from 'react';
import { motion } from 'motion/react';
import { Github } from 'lucide-react';

export function Navigation() {
  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="fixed top-0 left-0 right-0 z-50 px-6 py-4"
      style={{
        backgroundColor: 'rgba(15, 17, 21, 0.8)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid var(--surface-border)',
      }}
    >
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-semibold"
            style={{
              backgroundColor: 'var(--accent-primary)',
              color: 'var(--text-primary)',
            }}
          >
            च
          </div>
          <span className="font-semibold" style={{ color: 'var(--text-primary)' }}>
            Chatur
          </span>
        </div>

        {/* Links */}
        <div className="flex items-center gap-8">
          <a
            href="#features"
            className="text-sm transition-opacity hover:opacity-70 hidden md:block"
            style={{ color: 'var(--text-secondary)' }}
          >
            Features
          </a>
          <a
            href="#demo"
            className="text-sm transition-opacity hover:opacity-70 hidden md:block"
            style={{ color: 'var(--text-secondary)' }}
          >
            Demo
          </a>
          <a
            href="#developers"
            className="text-sm transition-opacity hover:opacity-70 hidden md:block"
            style={{ color: 'var(--text-secondary)' }}
          >
            Developers
          </a>
          <a
            href="https://github.com"
            className="flex items-center gap-2 text-sm transition-opacity hover:opacity-70"
            style={{ color: 'var(--text-secondary)' }}
            aria-label="GitHub Repository"
          >
            <Github className="w-4 h-4" />
            <span className="hidden sm:inline">GitHub</span>
          </a>
        </div>
      </div>
    </motion.nav>
  );
}