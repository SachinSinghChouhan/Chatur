import { useRef, useState } from 'react';
import { motion, useInView } from 'motion/react';
import { Download, Shield, Code, Layers, Terminal, Copy, Check } from 'lucide-react';

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button
      onClick={handleCopy}
      className="p-1 rounded hover:bg-white/10 transition-colors flex-shrink-0"
      title="Copy to clipboard"
    >
      {copied
        ? <Check className="w-3.5 h-3.5 text-green-400" />
        : <Copy className="w-3.5 h-3.5" style={{ color: 'var(--text-muted)' }} />
      }
    </button>
  );
}

function CommandLine({ command }: { command: string }) {
  return (
    <div
      className="flex items-center gap-2 px-3 py-2 rounded-md font-mono text-xs"
      style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}
    >
      <Terminal className="w-3 h-3 flex-shrink-0" style={{ color: 'var(--text-muted)' }} />
      <code className="flex-1 overflow-x-auto whitespace-nowrap" style={{ color: 'var(--text-secondary)' }}>
        {command}
      </code>
      <CopyButton text={command} />
    </div>
  );
}

function UbuntuCard() {
  return (
    <div
      className="rounded-xl border p-6 text-left"
      style={{ backgroundColor: 'var(--surface-card)', borderColor: 'var(--surface-border)' }}
    >
      <h3 className="font-semibold mb-1 text-lg" style={{ color: 'var(--text-primary)' }}>
        Ubuntu / Debian
      </h3>
      <p className="text-xs mb-4" style={{ color: 'var(--text-muted)' }}>
        Ubuntu 20.04+ / Debian 11+ (x64)
      </p>

      {/* .deb download */}
      <a
        href="https://github.com/SachinSinghChouhan/Chatur/releases/latest"
        target="_blank"
        rel="noopener noreferrer"
        className="w-full px-4 py-2.5 rounded-lg flex items-center justify-center gap-2 transition-all duration-200 hover:opacity-90 text-sm font-medium mb-4"
        style={{
          backgroundColor: 'var(--accent-primary)',
          color: 'white',
          textDecoration: 'none',
        }}
      >
        <Download className="w-4 h-4" />
        Download .deb
      </a>

      {/* Terminal install commands */}
      <p className="text-[11px] mb-2 font-medium" style={{ color: 'var(--text-muted)' }}>
        Or install via terminal:
      </p>
      <div className="space-y-1.5">
        <CommandLine command="wget https://github.com/SachinSinghChouhan/Chatur/releases/latest/download/chatur_1.0.3_amd64.deb" />
        <CommandLine command="sudo dpkg -i chatur_*_amd64.deb && sudo apt-get install -f" />
        <CommandLine command="chatur" />
      </div>
    </div>
  );
}

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
      id="download"
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

          {/* Download Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto mb-12">
            {/* Windows */}
            <div
              className="rounded-xl border p-6 text-left"
              style={{ backgroundColor: 'var(--surface-card)', borderColor: 'var(--surface-border)' }}
            >
              <h3 className="font-semibold mb-1 text-lg" style={{ color: 'var(--text-primary)' }}>
                Windows
              </h3>
              <p className="text-xs mb-4" style={{ color: 'var(--text-muted)' }}>
                Windows 10/11 (x64)
              </p>
              <a
                href="https://github.com/SachinSinghChouhan/Chatur/releases/latest/download/ChaturAssistant-windows-x64.exe"
                className="w-full px-4 py-2.5 rounded-lg flex items-center justify-center gap-2 transition-all duration-200 hover:opacity-90 text-sm font-medium"
                style={{
                  backgroundColor: 'var(--accent-primary)',
                  color: 'white',
                  textDecoration: 'none',
                }}
              >
                <Download className="w-4 h-4" />
                Download .exe
              </a>
              <p className="text-[11px] mt-3" style={{ color: 'var(--text-muted)' }}>
                Double-click to run — no installation needed
              </p>
            </div>

            {/* Ubuntu */}
            <UbuntuCard />
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