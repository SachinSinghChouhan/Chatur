import { useRef } from 'react';
import { motion, useInView } from 'motion/react';

const englishExamples = [
  { user: 'Open Chrome', chatur: 'Opening Google Chrome.' },
  { user: 'Set a timer for 10 minutes', chatur: 'Timer started — 10 minutes on the clock.' },
  { user: "What's 15% of 340?", chatur: 'That\'s 51.' },
  { user: 'Remind me to call mom at 6 PM', chatur: 'Reminder set for 6 PM today.' },
  { user: 'Find budget report in Documents', chatur: 'Found budget_report_Q4.xlsx in Documents.' },
];

function ChatBubble({ text, isUser }: { text: string; isUser: boolean }) {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className="max-w-xs px-4 py-3 rounded-lg"
        style={{
          backgroundColor: isUser ? 'var(--accent-primary)' : 'var(--surface-card)',
          color: 'var(--text-primary)',
          borderWidth: isUser ? '0' : '1px',
          borderColor: 'var(--surface-border)',
        }}
      >
        <p className="text-sm">{text}</p>
      </div>
    </div>
  );
}

export function DemoSection() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.1 });

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
            Natural Conversations
          </h2>
          <p className="text-lg" style={{ color: 'var(--text-secondary)' }}>
            Control your computer with just your voice
          </p>
        </motion.div>

        <div className="max-w-2xl mx-auto">
          {/* English Examples */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -20 }}
            transition={{ duration: 0.5, delay: 0.2, ease: 'easeOut' }}
          >
            <h3 className="text-xl mb-6 text-center" style={{ color: 'var(--text-primary)' }}>
              English
            </h3>
            <div
              className="p-6 rounded-lg border"
              style={{
                backgroundColor: 'var(--background)',
                borderColor: 'var(--surface-border)',
              }}
            >
              {englishExamples.map((example, index) => (
                <div key={index}>
                  <ChatBubble text={example.user} isUser={true} />
                  <ChatBubble text={example.chatur} isUser={false} />
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}