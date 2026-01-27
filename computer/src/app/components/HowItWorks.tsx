import React, { useRef } from 'react';
import { motion, useInView } from 'motion/react';
import { Ear, Mic, Brain, Zap, MessageCircle } from 'lucide-react';

const steps = [
  {
    icon: Ear,
    title: 'Wake Word Detection',
    description: 'Always listening for "Hey Chatur" to activate',
  },
  {
    icon: Mic,
    title: 'Speech Recognition',
    description: 'Converts your voice to text in English or Hindi',
  },
  {
    icon: Brain,
    title: 'Language Understanding',
    description: 'Interprets intent and context from your command',
  },
  {
    icon: Zap,
    title: 'Task Execution',
    description: 'Performs the requested action on your Windows PC',
  },
  {
    icon: MessageCircle,
    title: 'Voice Response',
    description: 'Replies back with natural speech synthesis',
  },
];

export function HowItWorks() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.2 });

  return (
    <section
      ref={ref}
      className="py-24 px-6"
      style={{ backgroundColor: 'var(--background-secondary)' }}
    >
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl mb-4" style={{ color: 'var(--text-primary)' }}>
            How It Works
          </h2>
          <p className="text-lg" style={{ color: 'var(--text-secondary)' }}>
            A simple pipeline that powers intelligent voice interaction
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
              transition={{ duration: 0.5, delay: index * 0.1, ease: 'easeOut' }}
              className="relative"
            >
              <div className="flex flex-col items-center text-center">
                {/* Icon */}
                <div
                  className="w-16 h-16 rounded-lg flex items-center justify-center mb-4 border"
                  style={{
                    backgroundColor: 'var(--surface-card)',
                    borderColor: 'var(--surface-border)',
                  }}
                >
                  <step.icon className="w-7 h-7" style={{ color: 'var(--accent-primary)' }} />
                </div>

                {/* Title */}
                <h3 className="mb-2" style={{ color: 'var(--text-primary)' }}>
                  {step.title}
                </h3>

                {/* Description */}
                <p className="text-sm" style={{ color: 'var(--text-muted)' }}>
                  {step.description}
                </p>

                {/* Connector line (not on last item) */}
                {index < steps.length - 1 && (
                  <div className="hidden lg:block absolute top-8 left-full w-full h-px">
                    <div
                      className="h-full w-full"
                      style={{ backgroundColor: 'var(--surface-border)' }}
                    />
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}