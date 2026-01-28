import React, { useEffect, useState } from 'react';
import { motion, useScroll, useTransform } from 'motion/react';
import { Mic, Github, Download } from 'lucide-react';

const TypewriterText = ({ text, delay = 0 }: { text: string; delay?: number }) => {
  const letters = Array.from(text);

  const container = {
    hidden: { opacity: 0 },
    visible: (i = 1) => ({
      opacity: 1,
      transition: { staggerChildren: 0.05, delayChildren: delay }
    })
  };

  const child = {
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        damping: 12,
        stiffness: 100,
      }
    },
    hidden: {
      opacity: 0,
      y: 20,
      transition: {
        type: "spring",
        damping: 12,
        stiffness: 100,
      }
    }
  };

  return (
    <motion.span
      style={{ display: "inline-block" }}
      variants={container}
      initial="hidden"
      animate="visible"
    >
      {letters.map((letter, index) => (
        <motion.span variants={child} key={index}>
          {letter === " " ? "\u00A0" : letter}
        </motion.span>
      ))}
    </motion.span>
  );
};

export function Hero() {
  const { scrollY } = useScroll();
  const y1 = useTransform(scrollY, [0, 500], [0, 200]);
  const y2 = useTransform(scrollY, [0, 500], [0, -150]);

  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 py-20 pt-32 overflow-hidden">
      {/* Cinematic Background Particles */}
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        <motion.div
          style={{ y: y1, opacity: 0.2 }}
          className="absolute top-20 left-10 w-64 h-64 bg-slate-500/20 rounded-full blur-3xl"
        />
        <motion.div
          style={{ y: y2, opacity: 0.1 }}
          className="absolute bottom-20 right-10 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl"
        />
        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-5"></div>
      </div>

      <div className="relative z-10 max-w-4xl mx-auto text-center">
        {/* Microphone Icon with Subtle Pulse */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="mb-12 flex justify-center"
        >
          <div className="relative">
            <motion.div
              animate={{ scale: [1, 1.05, 1], boxShadow: ["0 0 0px rgba(99,102,241,0)", "0 0 20px rgba(99,102,241,0.3)", "0 0 0px rgba(99,102,241,0)"] }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
              className="w-24 h-24 rounded-full bg-[var(--surface-card)] border border-[var(--surface-border)] flex items-center justify-center backdrop-blur-sm z-10 relative"
            >
              <Mic className="w-10 h-10 text-[var(--accent-primary)]" />
            </motion.div>
            {/* Animated Rings */}
            {[1, 2].map((ring) => (
              <motion.div
                key={ring}
                initial={{ opacity: 0, scale: 1 }}
                animate={{ scale: 1.5, opacity: 0 }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  delay: ring * 1,
                  ease: "easeOut",
                }}
                className="absolute inset-0 rounded-full border border-[var(--accent-primary)]"
              />
            ))}
          </div>
        </motion.div>

        {/* Headline with Typewriter Effect */}
        <h1
          className="text-5xl md:text-6xl lg:text-7xl mb-6 tracking-tight font-bold"
          style={{ color: 'var(--text-primary)' }}
        >
          {mounted && <TypewriterText text="Meet Chatur" delay={0.5} />}
        </h1>

        {/* Subheading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1.5, ease: 'easeOut' }}
          className="text-xl md:text-2xl mb-12 max-w-2xl mx-auto"
          style={{ color: 'var(--text-secondary)' }}
        >
          <p>A bilingual personal voice assistant for Windows.</p>
          <p className="mt-2 text-[var(--accent-primary)]">Speak naturally in English or Hindi.</p>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 2, ease: 'easeOut' }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <button
            className="group px-8 py-4 rounded-lg flex items-center gap-2 transition-all duration-300 hover:scale-105 hover:shadow-[0_0_20px_rgba(99,102,241,0.5)] relative overflow-hidden"
            style={{
              backgroundColor: 'var(--accent-primary)',
              color: 'var(--text-primary)',
            }}
          >
            <span className="relative z-10 flex items-center gap-2">
              <Download className="w-5 h-5" />
              Download for Windows
            </span>
            <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
          </button>
          <button
            className="px-8 py-4 rounded-lg flex items-center gap-2 border transition-all duration-200 hover:bg-[var(--surface-card)] hover:border-[var(--accent-primary)]"
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
          transition={{ duration: 0.6, delay: 2.2, ease: 'easeOut' }}
          className="mt-8 text-sm"
          style={{ color: 'var(--text-muted)' }}
        >
          Open source • Privacy-first • Local processing
        </motion.p>
      </div>
    </section>
  );
}