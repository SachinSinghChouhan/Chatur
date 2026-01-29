import { useRef } from 'react';
import { motion, useInView } from 'motion/react';
import { Ear, Mic, Brain, Zap, MessageCircle } from 'lucide-react';

const steps = [
  {
    icon: Ear,
    title: 'Wake Word',
    description: 'Always listening for "Hey Chatur"',
  },
  {
    icon: Mic,
    title: 'Speech',
    description: 'Converts your voice to text',
  },
  {
    icon: Brain,
    title: 'Intent',
    description: 'Understands context & meaning',
  },
  {
    icon: Zap,
    title: 'Action',
    description: 'Executes command on Windows',
  },
  {
    icon: MessageCircle,
    title: 'Reply',
    description: 'Speaks back naturally',
  },
];

export function HowItWorks() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.3 });

  return (
    <section
      ref={ref}
      className="py-24 px-6 relative"
      style={{ backgroundColor: 'var(--background-secondary)' }}
    >
      <div className="max-w-6xl mx-auto relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="text-center mb-20"
        >
          <h2 className="text-4xl md:text-5xl mb-4 font-bold" style={{ color: 'var(--text-primary)' }}>
            System Pipeline
          </h2>
          <p className="text-lg" style={{ color: 'var(--text-secondary)' }}>
            Real-time processing flow from speech to action
          </p>
        </motion.div>

        {/* Animated Connecting Line (Desktop) */}
        <div className="hidden lg:block absolute top-[13.5rem] left-0 w-full h-1 z-0">
          <svg className="w-full h-20 overflow-visible">
            <motion.path
              d="M 100,10 L 1100,10"
              fill="none"
              stroke="var(--accent-primary)"
              strokeWidth="2"
              strokeDasharray="10 10"
              initial={{ pathLength: 0, opacity: 0 }}
              animate={isInView ? { pathLength: 1, opacity: 0.5 } : { pathLength: 0, opacity: 0 }}
              transition={{ duration: 2, ease: "easeInOut", delay: 0.5 }}
            />
          </svg>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 relative z-10">
          {steps.map((step, index) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 30 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
              transition={{ duration: 0.5, delay: index * 0.2, ease: 'easeOut' }}
              className="relative group"
            >
              <div className="flex flex-col items-center text-center">
                {/* Icon Container with Glow */}
                <div className="relative mb-6">
                  <motion.div
                    className="absolute inset-0 rounded-xl blur-lg opacity-0 group-hover:opacity-50 transition-opacity duration-500"
                    style={{ backgroundColor: 'var(--accent-primary)' }}
                  />
                  <div
                    className="w-20 h-20 rounded-xl flex items-center justify-center border relative z-10 transition-transform duration-300 group-hover:scale-110"
                    style={{
                      backgroundColor: 'var(--surface-card)',
                      borderColor: 'var(--surface-border)',
                    }}
                  >
                    <step.icon className="w-8 h-8" style={{ color: 'var(--accent-primary)' }} />
                  </div>
                </div>

                {/* Step Number Badge */}
                <div className="px-2 py-0.5 rounded-full text-[10px] font-bold tracking-widest uppercase mb-2" style={{ backgroundColor: 'rgba(255,255,255,0.05)', color: 'var(--text-muted)' }}>
                  Step 0{index + 1}
                </div>

                {/* Title */}
                <h3 className="mb-2 font-semibold text-lg" style={{ color: 'var(--text-primary)' }}>
                  {step.title}
                </h3>

                {/* Description */}
                <p className="text-sm leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
                  {step.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}