import { useEffect, useState } from 'react';
import { motion } from 'motion/react';
import { Github } from 'lucide-react';

export function Navigation() {
  const [version, setVersion] = useState<string | null>(null);

  useEffect(() => {
    fetch('https://api.github.com/repos/SachinSinghChouhan/Chatur/releases/latest')
      .then(r => r.json())
      .then(d => { if (d.tag_name) setVersion(d.tag_name); })
      .catch(() => {});
  }, []);

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
        {/* Logo + version badge */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-semibold"
              style={{ backgroundColor: 'var(--accent-primary)', color: 'var(--text-primary)' }}
            >
              च
            </div>
            <span className="font-semibold" style={{ color: 'var(--text-primary)' }}>
              Chatur
            </span>
          </div>
          {version && (
            <span
              className="text-[11px] px-2 py-0.5 rounded-full font-mono hidden sm:inline-block"
              style={{
                backgroundColor: 'rgba(99,102,241,0.15)',
                color: 'var(--accent-primary)',
                border: '1px solid rgba(99,102,241,0.3)',
              }}
            >
              {version}
            </span>
          )}
        </div>

        {/* Links */}
        <div className="flex items-center gap-6">
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
            href="https://github.com/SachinSinghChouhan/Chatur"
            target="_blank"
            rel="noopener noreferrer"
            className="transition-opacity hover:opacity-70 hidden md:block"
            aria-label="GitHub"
          >
            <Github className="w-5 h-5" style={{ color: 'var(--text-secondary)' }} />
          </a>
          <a
            href="#download"
            className="px-4 py-1.5 rounded-lg text-sm font-medium transition-all hover:opacity-90"
            style={{
              backgroundColor: 'var(--accent-primary)',
              color: 'white',
            }}
          >
            Download
          </a>
        </div>
      </div>
    </motion.nav>
  );
}
