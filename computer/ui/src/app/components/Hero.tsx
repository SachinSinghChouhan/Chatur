import { useEffect, useState } from 'react';
import { motion, useScroll, useTransform, AnimatePresence } from 'motion/react';
import { Mic } from 'lucide-react';

const EXAMPLE_COMMANDS = [
  { command: '"Set a timer for 10 minutes"',   response: 'Timer started — 10 minutes.' },
  { command: '"Open Chrome"',                   response: 'Opening Google Chrome.' },
  { command: '"What\'s 15% of 340?"',           response: 'That\'s 51.' },
  { command: '"Remind me to call mom at 6 PM"', response: 'Reminder set for 6 PM.' },
];

function CyclingCommand() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setIndex(i => (i + 1) % EXAMPLE_COMMANDS.length), 3000);
    return () => clearInterval(id);
  }, []);

  const { command, response } = EXAMPLE_COMMANDS[index];

  return (
    <div
      className="rounded-xl border p-4 text-left max-w-md mx-auto"
      style={{ backgroundColor: 'var(--surface-card)', borderColor: 'var(--surface-border)' }}
    >
      <div className="flex items-center gap-2 mb-3">
        <Mic className="w-3.5 h-3.5 flex-shrink-0" style={{ color: 'var(--accent-primary)' }} />
        <span className="text-xs font-medium" style={{ color: 'var(--text-muted)' }}>You say</span>
      </div>
      <AnimatePresence mode="wait">
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -6 }}
          transition={{ duration: 0.3 }}
        >
          <p className="text-sm font-medium mb-2" style={{ color: 'var(--text-primary)' }}>
            {command}
          </p>
          <div className="flex items-center gap-2">
            <div className="w-5 h-5 rounded flex items-center justify-center text-[10px] font-bold flex-shrink-0"
              style={{ backgroundColor: 'var(--accent-primary)', color: 'white' }}>
              च
            </div>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{response}</p>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

const TypewriterText = ({ text, delay = 0 }: { text: string; delay?: number }) => {
  const letters = Array.from(text);

  const container = {
    hidden: { opacity: 0 },
    visible: () => ({
      opacity: 1,
      transition: { staggerChildren: 0.05, delayChildren: delay }
    })
  };

  const child = {
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring" as const,
        damping: 12,
        stiffness: 100,
      }
    },
    hidden: {
      opacity: 0,
      y: 20,
      transition: {
        type: "spring" as const,
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
          <p>A personal voice assistant for Windows & Ubuntu.</p>
          <p className="mt-2 text-[var(--accent-primary)]">Speak naturally to control your computer.</p>
        </motion.div>

        {/* Cycling example commands */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 2.0, ease: 'easeOut' }}
          className="mt-10"
        >
          <CyclingCommand />
        </motion.div>

        {/* Tagline */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 2.5, ease: 'easeOut' }}
          className="mt-8 flex flex-wrap justify-center gap-x-4 gap-y-1 text-sm"
          style={{ color: 'var(--text-muted)' }}
        >
          <span>Open source</span>
          <span>•</span>
          <span>Privacy-first</span>
          <span>•</span>
          <span>Works offline</span>
        </motion.div>

        {/* Download CTA */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 2.8, ease: 'easeOut' }}
          className="mt-8"
        >
          <a
            href="#download"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all hover:opacity-90"
            style={{ backgroundColor: 'var(--accent-primary)', color: 'white' }}
          >
            Download Free
          </a>
        </motion.div>
      </div>
    </section>
  );
}